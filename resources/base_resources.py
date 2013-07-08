from tastypie.resources import Resource, ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from alpheus.serializers import PrettyJSONSerializer
from tastypie.exceptions import BadRequest


class TestResource(ModelResource):
    class Meta:
        serializer = PrettyJSONSerializer()


DATE_TYPE_DAY = 'd'
DATE_TYPE_WEEK = 'w'
DATE_TYPE_MONTH = 'm'

DATA_TYPE_YEAR = 'year'
DATA_TYPE_GROUP = 'group'
DATA_TYPE_GRAPH = 'graph'

# Base Model Resource
class MainBaseResource(ModelResource):
    class Meta:
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        serializer = PrettyJSONSerializer()
        include_resource_uri = False
        columns = []

    # Format output
    def alter_list_data_to_serialize(self, request, data):
        if isinstance(data,dict):
            return data['objects']

    # Disables paging
    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                                    **self.remove_api_resource_names(kwargs))



        bundles = []

        for obj in objects:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle))

        serialized = {}
        serialized[self._meta.collection_name] = bundles
        serialized = self.alter_list_data_to_serialize(request, serialized)

        return self.create_response(request, serialized)


    def set_columns(self, request, column_names):

        column_width = request.GET.get('column_width', '50,50').split(',')
        column_border_y = request.GET.get('column_border_y', 'ytd')
        align = request.GET.get('align', 'left')

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
                    'dataIndex': value,
                    'align': 'center',
                }
            except:
                try:
                    column = value
                    dic = {
                        'dataIndex': column[0],
                        'text': column[1].title().replace('_', ' '),
                        'align': 'center',
                    }
                except:
                    raise
            if column == column_border_y:
                dic['tdCls'] = 'horizonal-border-column'

            if key == 0:
                dic['width'] = column_width[0]
                dic['align'] = 'left'
            else:
                dic['width'] = column_width[1]
                dic['align'] = align

            columns.append(dic)

        return columns


    def check_params(self, params, filters):
        for param in params:
            if not param in filters:
                raise BadRequest("Param '%s' is mandatory" % param)


    def dehydrate(self, bundle):

        """
        Adds support for double underscore in the Meta.fields
        Currently it only supports two levels
        """
        to_delete = []

        for row in self._meta.fields:
            fields = row.split('__')
            if len(fields) > 1:
                if len(fields) == 3:
                    bundle.data[fields[0]] = bundle.data[fields[0]].\
                                        data[fields[1]].data[fields[2]]

                if len(fields) == 2:
                    if fields[1] == 'name':
                        bundle.data[fields[0]] = bundle.data[fields[0]].data[fields[1]]
                    else:
                        try:
                            bundle.data[fields[1]] = bundle.data[fields[0]].data[fields[1]]
                        except:
                            print 'skipping', fields

        # make sure all Decimals have two decimal places
        from decimal import *
        for key, val in bundle.data.iteritems():
            if isinstance(val, Decimal):
                bundle.data[key] = Decimal("%.2f" % val)

        """
        Saving the field names so we can create column names for tables later
        """
        for name, value in bundle.data.iteritems():
            try:
                if name not in self._meta.columns and name != 'id':
                    self._meta.columns.append(name)
            except:
                pass

        return bundle


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

        from django.db.models import Q
        import operator
        from types import *

        """
        Adds support for:
        1. negation filtering: value_date__year!=2013
        2. multiple filtering value_date__year=2013,2012
        """

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




# v2
class MainBaseResource2(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        allowed_fields = []

    def get_month_list(self):
        import calendar
        months = []
        for month in range(1, 13):
            months.append(calendar.month_abbr[month].lower())
        return months

    #def dispatch(self, request_type, request, **kwargs):
    def get_object_list(self, request):

    #def apply_filters(self, request, applicable_filters):

        self.data_type = request.GET.get("data_type", False)
        self.date_type = request.GET.get("date_type", False)

        if self.data_type == 'year':
            try:
                extra_fields = request.GET.get("extra_fields", []).split(',')
            except:
                extra_fields = []
            self.year = {
                'value': request.GET.get("value", 0),
                'date': request.GET.get("date", 0),
                'title': request.GET.get("title", 0),
                'extra_fields': extra_fields,
            }
            self.external_fields = [
                'id',
                self.year['title'],
                self.year['value'],
                self.year['date'],
            ] + self.year['extra_fields']

        else:
            self.external_fields = []
            fields = request.GET.get("fields", False)
            if fields:
                self.external_fields = fields.split(',')

        #return super(MainBaseResource2, self).dispatch(request_type, request, **kwargs)
        #return super(MainBaseResource2, self).apply_filters(self, request, applicable_filters)

        #def get_object_list(self, request):

        """
        Only fetches the specified columns
        Automatically sets `select_related`
        Sets the verbose name of the field to `column_names`
        """

        from django.db import models

        objects = super(MainBaseResource2, self).get_object_list(request)

        from django.utils.datastructures import SortedDict
        self.column_names = SortedDict()

        self.select_related = []

        if len(self.external_fields):
            self.internal_fields = self.external_fields
        else:
            self.internal_fields = self._meta.allowed_fields


        # do distinct on m2m filters
        """
        not used atm, but works
        Use this later and make distinct true by default when there is an m2m filter
        distinct = False
        for field in self.filters:
            try:
                m2m = objects.model._meta.get_field_by_name(field)[0]
                if m2m.get_internal_type() == 'ManyToManyField':
                    #distinct = True
                    pass
            except:
                pass
        """

        # Removes fields that do not exist for this model
        # Like fields that are model methods
        """
        only_fields = []
        for field in objects.model._meta.fields:
            if field.name in self.internal_fields:
                only_fields.append(field.name)
        """
        only_fields = []
        for field in objects.model._meta.fields:
            for internal_field in self.internal_fields:
                try:
                    related_field = internal_field.split('__')
                    if field.name == related_field[0]:
                        only_fields.append(field.name)
                except:
                    pass

        objects = objects.only(*only_fields)

        for field in self.internal_fields:

            try:
                related_fields = field.split('__')
            except:
                related_fields = []

            if len(related_fields) > 1:

                self.select_related.append(related_fields[0])

                model_name = related_fields[0].replace('_', ' ').title() \
                                                            .replace(' ', '')
                model = models.get_model('app', model_name)
                for rel_field in model._meta._fields():
                    if related_fields[1] == rel_field.name:
                        self.column_names[field] = rel_field.verbose_name \
                                                                .capitalize()
            else:
                for meta_field in objects.model._meta._fields():
                    if field == meta_field.name:
                        self.column_names[field] = meta_field.verbose_name \
                                                                .capitalize()

        if len(self.select_related):
            objects = objects.select_related(*self.select_related)

        if request.GET.get('distinct', False) == 'true':
            objects = objects.distinct()

        return objects

    def full_dehydrate(self, bundle, for_list=False):
        """
        Given a bundle with an object instance, extract the information from it
        to populate the resource.
        """
        # Dehydrate each field supplied in the `fields` parameter
        for field_name, field_object in self.fields.items():

            # A touch leaky but it makes URI resolution work.
            if getattr(field_object, 'dehydrated_type', None) == 'related':
                field_object.api_name = self._meta.api_name
                field_object.resource_name = self._meta.resource_name

            # Check for an optional method to do further dehydration.
            method = getattr(self, "dehydrate_%s" % field_name, None)

            if method:
                bundle.data[field_name] = method(bundle)

        bundle = self.dehydrate(bundle)
        return bundle

    def dehydrate(self, bundle):

        for row in self.internal_fields:
            try:
                fields = row.split('__')
            except:
                pass
            if len(fields) == 1:
                try:
                    bundle.data[row] = getattr(bundle.obj, fields[0])()
                except:
                    bundle.data[row] = getattr(bundle.obj, fields[0])
            elif len(fields) == 2:
                try:
                    bundle.data[row] = getattr(getattr(bundle.obj, \
                                                fields[0]), fields[1])
                except:
                    raise Exception("'%s' not found." % row)
            elif len(fields) == 3:
                try:
                    bundle.data[row] = getattr(getattr(getattr(bundle.obj, \
                                            fields[0]), fields[1]), fields[2])
                except:
                    raise Exception("'%s' not found." % row)

            # display actual values for `choices` fields
            try:
                method = getattr(bundle.obj, "get_%s_display" % fields[0], None)
                bundle.data[fields[0]] = method()
            except:
                pass

        # make sure all Decimals have two decimal places
        from decimal import *
        for key, val in bundle.data.iteritems():
            if isinstance(val, Decimal):
                bundle.data[key] = Decimal("%.2f" % val)

        return bundle


    def get_columns(self, request, column_names):

        column_width = request.GET.get('column_width', '50,50').split(',')
        column_border_y = request.GET.get('column_border_y', 'ytd')
        align = request.GET.get('align', 'left')

        columns = []
        counter = 0
        for key, value in self.column_names.iteritems():

            dic = {
                'dataIndex': key,
                'text': value,
            }
            if key == column_border_y:
                dic['tdCls'] = 'horizonal-border-column'

            if counter == 0:
                dic['width'] = column_width[0]
                dic['align'] = 'left'
            else:
                dic['width'] = column_width[1]
                dic['align'] = align

            columns.append(dic)
            counter += 1

        return columns


    def alter_list_data_to_serialize(self, request, data):


        # format value_date for months
        if self.date_type == DATE_TYPE_MONTH:
            pass
            #for key, val in enumerate(data['objects']):
            #    data['objects'][key].data['value_date'] = data['objects'][key] \
            #                                 .data['value_date'].strftime("%b %Y")


        if self.data_type == DATA_TYPE_YEAR:
            import calendar
            value = self.year['value']
            date = self.year['date']
            name = self.year['title']
            extra_fields = self.year['extra_fields']

            categories = set([row.data[name] for row in data['objects']])

            months = []
            for category in categories:
                dic = {name: category}
                for row in data['objects']:
                    if row.data[name] == category:
                        month = row.data[date].month
                        month_name = calendar.month_abbr[month].lower()
                        dic[month_name] = row.data[value]
                        for extra_field in extra_fields:
                            dic[extra_field] = row.data[extra_field]
                months.append(dic)

            columns = [name] + self.get_month_list() + extra_fields
            return {
                'columns': self.set_columns(request, columns),
                'rows': months,
            }

        else:
            total = request.GET.get("total", False)
            if total:
                total_dic = {self.internal_fields[0]: 'Total'}
                for field in self.internal_fields[1:]:
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

            return {
                'columns': self.set_columns(request, self.internal_fields),
                'rows': data['objects'],
            }



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




