from tastypie.resources import Resource, ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from alpheus.serializers import PrettyJSONSerializer
from alpheus.specifiedfields import SpecifiedFields
from tastypie.exceptions import BadRequest

import collections

class StandardBaseResource(ModelResource):
    class Meta:
        serializer = PrettyJSONSerializer()


    def alter_list_data_to_serialize(self, request, data):
        return data['objects']

DATE_TYPE_DAY = 'd'
DATE_TYPE_WEEK = 'w'
DATE_TYPE_MONTH = 'm'

DATA_TYPE_YEAR = 'year'
DATA_TYPE_GROUP = 'group'
DATA_TYPE_GRAPH = 'graph'
DATA_TYPE_TOTAL = 'total'
DATA_TYPE_COMPACT = 'compact'
DATA_TYPE_LIST = 'list'

# Base Model Resource
class MainBaseResource(SpecifiedFields):
    class Meta:
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        serializer = PrettyJSONSerializer()
        include_resource_uri = False
        columns = []

    """
    Allow all 'order_by' by default
    """
    def apply_sorting(self, obj_list, options=None):
        return obj_list.order_by()

    """
    Allow all filters by default
    """
    def check_filtering(self, field_name, filter_type='exact', filter_bits=None):
        return [self.fields[field_name].attribute]

    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                                    **self.remove_api_resource_names(kwargs))

        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, \
                                            resource_uri=self.get_resource_uri(), \
                                            limit=self._meta.limit, \
                                            max_limit=self._meta.max_limit, \
                                            collection_name=self._meta.collection_name)

        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = []


        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)


    def check_params(self, params, filters):
        for param in params:
            if not param in filters:
                raise BadRequest("Param '%s' is mandatory" % param)


    def build_filters(self, filters=None):

        """
        Adds support for negation filtering
        """
        if not filters:
            return filters

        applicable_filters = {}
        self.filters = filters

        # Normal filtering
        filter_params = dict([(x, filters[x]) for x in filter(lambda x: not x.endswith('!'), filters)])
        applicable_filters['filter'] = super(MainBaseResource, self).build_filters(filter_params)

        # Exclude filtering
        exclude_params = dict([(x[:-1], filters[x]) for x in filter(lambda x: x.endswith('!'), filters)])
        applicable_filters['exclude'] = super(MainBaseResource, self).build_filters(exclude_params)

        return applicable_filters

    def apply_filters(self, request, applicable_filters):

        """
        Adds support for:
        1. negation filtering: value_date__year!=2013
        2. multiple filtering value_date__year=2013,2012
        """

        from django.db.models import Q
        import operator
        from types import *

        objects = self.get_object_list(request)

        f = applicable_filters.get('filter')

        if f:
            # Q Filters for multiple values (1,2,3 etc)
            q_filters = []
            for key, val in f.iteritems():
                string = str(val)
                if ',' in string:
                    for excl_filter in string.split(','):
                        q_filters.append((key, excl_filter))

            q_list = [Q(x) for x in q_filters]
            for x in q_filters:
                try:
                    del f[x[0]]
                except:
                    pass
            if q_list:
                objects = objects.filter(reduce(operator.or_, q_list), **f)
            else:
                objects = objects.filter(**f)

        e = applicable_filters.get('exclude')
        if e:
            objects = objects.exclude(**e)
        return objects



    def get_month_list(self):
        import calendar
        months = []
        for month in range(1, 13):
            months.append(calendar.month_abbr[month].lower())
        return months

    def dispatch(self, request_type, request, **kwargs):

        self.data_type = request.GET.get("data_type", False)
        #self.date_type = request.GET.get("date_type", False)

        self.specified_fields = []
        try:
            self.extra_fields = request.GET.get("extra_fields", []).split(',')
            self.specified_fields += self.extra_fields
        except:
            self.extra_fields = []

        self.value = request.GET.get("value", False)
        if self.value:
            self.specified_fields.append(self.value)

        self.date = request.GET.get("date", False)
        if self.date:
            self.specified_fields.append(self.date)

        title = request.GET.get("title", False)
        if title:
            self.title = title.split(',')
        else:
            self.title = []

        if len(self.title):
            self.specified_fields += self.title

        self.y1 = request.GET.get("y1", False)
        if self.y1:
            self.specified_fields.append(self.y1)

        self.y2 = request.GET.get("y2", False)
        if self.y2:
            self.specified_fields.append(self.y2)

        return super(MainBaseResource, self).dispatch(request_type, request, **kwargs)

    def get_object_list(self, request):

        """ Set verbose column names """

        # @TODO: Use another hook for this
        objects = super(MainBaseResource, self).get_object_list(request)

        from django.utils.datastructures import SortedDict
        self.column_names = SortedDict()

        for field in self.specified_fields:

            try:
                f = field.split('__')[0]
            except:
                continue

            """
            find another way that does not produce extra queries

            try:
                self.column_names[f] = objects[0].objects._meta \
                        .get_field_by_name(f)[0].verbose_name.capitalize()
            except:
                pass
            """

        return objects


    def dehydrate(self, bundle):

        """ Round all Decimals to two decimal places """

        bundle = super(MainBaseResource, self).dehydrate(bundle)

        # @TODO: make this support multiple levels
        from decimal import *
        for key, val in bundle.data.iteritems():

            if isinstance(val, Decimal):
                bundle.data[key] = Decimal("%.2f" % val)

        return bundle


    def get_columns(self, request, column_names):

        column_width = request.GET.get('column_width', '50,50').split(',')
        #column_border_y = request.GET.get('column_border_y', 'ytd')
        align = request.GET.get('align', 'left')

        columns = []
        counter = 0
        for key, value in self.column_names.iteritems():

            dic = {
                'dataIndex': key,
                'text': value,
                'menuDisabled': True,
            }
            #if key == column_border_y:
            #    dic['tdCls'] = 'horizonal-border-column'

            if 'ytd' in value.lower():
                dic['tdCls'] = 'ytd-column'

            if counter == 0:
                dic['width'] = column_width[0]
                dic['align'] = 'left'
            else:
                dic['width'] = column_width[1]
                dic['align'] = align

            columns.append(dic)
            counter += 1

        return columns


    def set_columns(self, request, column_names):

        column_width = request.GET.get('column_width', '50,50').split(',')
        #column_border_y = request.GET.get('column_border_y', 'ytd')
        align = request.GET.get('align', 'left')
        total = request.GET.get('total', False) == 'true'

        columns = []
        for key, value in enumerate(column_names):

            if value == 'id':
                continue

            try:
                split = value.split('__')
                try:
                    if split[1] == 'name':
                        column = split[0]
                    else:
                        column = split[1]
                except:
                    column = split[0]
                dic = {
                    'text': column.title().replace('_', ' '),
                    'dataIndex': value.lower(),
                    'align': 'center',
                    'flex': True,
                    'menuDisabled': True,
                }
            except:
                try:
                    column = value
                    dic = {
                        'dataIndex': column[0].lower(),
                        'text': column[1].title().replace('_', ' '),
                        'align': 'center',
                        'menuDisabled': True,
                    }
                except:
                    raise
            #if column == column_border_y:
            #    dic['tdCls'] = 'horizonal-border-column'

            if 'ytd' in value.lower():
                dic['tdCls'] = 'ytd-column'

            if total and key != 0:
                dic['summaryType'] = 'sum'

            if key == 0:
                dic['width'] = column_width[0]
                dic['align'] = 'left'
            else:
                dic['width'] = column_width[1]
                dic['align'] = align

            columns.append(dic)

        return columns


    def alter_list_data_to_serialize(self, request, data):
    
        print 'ALTER LIST DATA', self.data_type, request.GET.get('data_type', False)

        if request.GET.get('data_type', False) == DATA_TYPE_YEAR:
            import calendar

            if self.y1 and len(self.title):


                newlist = []
                categories = {}
                for month in range(1, 13):
                    for row in data['objects']:
                        try:
                            categories[row.data[self.title[0]]][row.data[self.date].month] =  float(row.data[self.y1])
                        except:
                            categories[row.data[self.title[0]]] = {}
                            categories[row.data[self.title[0]]][row.data[self.date].month] = float(row.data[self.y1])

                #categories = collections.OrderedDict(sorted(categories.items()))

                for key, val in categories.iteritems():
                    dic = {
                        'name': key,
                        'data': val.values(),
                    }
                    newlist.append(dic)

                # create columns
                columns = []
                for month in range(1, 13):
                    abbr = calendar.month_abbr[month]
                    columns.append(abbr)

                return {
                    'columns': columns,
                    'objects': newlist,
                }

            elif len(self.title):

                categories = set([row.data[self.title[0]] for row in data['objects']])

                months = []
                for category in categories:
                    dic = {self.title[0]: category}
                    for row in data['objects']:
                        if row.data[self.title[0]] == category:
                            month = row.data[self.date].month
                            month_name = calendar.month_abbr[month].lower()
                            dic[month_name] = row.data[self.value]
                            for extra_field in self.extra_fields:
                                dic[extra_field] = row.data[extra_field]
                    months.append(dic)

                columns = [self.title[0]] + self.get_month_list() + self.extra_fields

            else:
            
                value = request.GET.get('value', False)

                categories = set([row.data[self.date].year for row in data['objects']])
                categories = sorted(categories, reverse=True)

                months = []
                for category in categories:
                    dic = {'year': category}
                    dic['id'] = category
                    for row in data['objects']:

                        if row.data[self.date].year == category:
                            month = row.data[self.date].month
                            month_name = calendar.month_abbr[month].lower()
                            dic[month_name] = row.data[value]
                            for extra_field in self.extra_fields:
                                dic[extra_field] = row.data[extra_field]
                    months.append(dic)

                columns = ['Year'] + self.get_month_list() + self.extra_fields

            return {
                'columns': self.set_columns(request, columns),
                'rows': months,
            }

        elif self.data_type == DATA_TYPE_GRAPH:

            from time import mktime

            if self.y1 and self.y2 and request.GET.get("graph_type", False) == False and self.date:

                y1 = []
                y2 = []
                for row in data['objects']:
                    date = int(mktime(row.data[self.date].timetuple())) * 1000
                    y1.append([date, float(row.data[self.y1])])
                    y2.append([date, float(row.data[self.y2])])
                return [{
                    'data': y1,
                    #'yAxis': 0,
                },{
                    'data': y2,
                    #'yAxis': 1,
                }]

            elif self.y1 and len(self.title):

                y1 = []
                for row in data['objects']:
                    y1.append({
                        'y': float(row.data[self.y1]), #@TODO: Perm fix for float bug
                        'name': ' '.join([row.data[title] for title in self.title]),
                    })
                return {'objects': [{'data': y1}]}

            elif self.y1 and self.date:

                extracted = []
                for row in data['objects']:
                    date = int(mktime(row.data[self.date].timetuple())) * 1000
                    extracted.append([int(date), float(row.data[self.y1])])
                data['objects'] = extracted
            else:
                raise Exception("Mandatory parameter(s) not passed")

            return {'objects': [{'data': data['objects']}]}


        elif self.data_type == DATA_TYPE_TOTAL:
            total_dic = {self.specified_fields[0]: 'Total'}
            for field in self.specified_fields[1:]:
                total_dic[field] = 0
                for val in data['objects']:
                    try:
                        if isinstance(val.data[field], basestring):
                            total_dic[field] = ''
                        else:
                            total_dic[field] += val.data[field]
                    except:
                        pass
            data['objects'].insert(0, {}) # empty row is separator
            data['objects'].insert(0, total_dic)

        elif self.data_type == DATA_TYPE_COMPACT:
            response = []
            for row in data['objects']:
                lis = []
                for field in self.specified_fields:
                    try:
                        lis.append(row.data[field])
                    except:
                        pass
                response.append(lis)
            data['objects'] = response


        elif self.data_type == DATA_TYPE_LIST:

            response = []

            for row in data['objects']:
                dic = {}
                for field in self.specified_fields:
                    dic[field] = row.data[field]
                response.append(dic)
            return response


        if self.specified_fields:
            return {
                'columns': self.set_columns(request, self.specified_fields),
                'fields': self.specified_fields,
                'rows': data['objects'],
            }
        else:

            return data['objects']



from mptt.templatetags.mptt_tags import cache_tree_children

class TreeBaseResource(ModelResource):

    def get_node_data(self, obj):
        """
        Controls the data structure of the output

        This needs to be overridden by the child class
        """
        raise NotImplementedError()


    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                                    **self.remove_api_resource_names(kwargs))

        # Caches the queryset so django-mptt doesn't hit the database
        # unnecessarily
        objects = cache_tree_children(objects)

        bundles = []

        for obj in objects:
            data = self.get_node_data(obj)
            bundle = self.build_bundle(data=data, obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle))

        serialized = {}
        serialized[self._meta.collection_name] = bundles
        serialized = self.alter_list_data_to_serialize(request, serialized)
        return self.create_response(request, serialized)


class UserObjectsOnlyAuthorization(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    """
    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming their auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")
    """
    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user




