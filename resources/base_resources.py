from tastypie.resources import Resource, ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from alpheus.serializers import PrettyJSONSerializer
from tastypie.exceptions import BadRequest


# Base Model Resource - IS THIS USED?
class MainBaseResource2(ModelResource):
    class Meta:
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        serializer = PrettyJSONSerializer()
        include_resource_uri = False

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




    def check_params(self, params, filters):

        for param in params:
            if not param in filters:
                raise BadRequest("Param '%s' not mandatory" % param)

    # fund param is mandatory
    def build_filters(self, filters=None):
        self.check_params(params, filters)
        return super(FundPerfYearlyResource, self).build_filters(filters)

# Base Model Resource
class MainBaseResource(ModelResource):
    class Meta:
        #authentication = SessionAuthentication()
        #authorization = DjangoAuthorization()
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

    def set_columns(self, column_names, width=False):

        # first column is 0, the rest are 1
        if not width:
            width = {}
            width[0] = 50
            width[1] = 50


        columns = []
        for key, value in enumerate(column_names):

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
                    'dataIndex': column,
                }
            except:
                try:
                    column = value
                    dic = {
                        'dataIndex': column[0],
                        'text': column[1].title().replace('_', ' '),
                    }
                except:
                    raise
            if key == 0:
                dic['width'] = width[0]
            else:
                dic['width'] = width[1]
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
                    #if fields[2] == 'name':
                    #    name = fields[1]
                    #else:
                    #    name = fields[2]
                    bundle.data[fields[0]] = bundle.data[fields[0]].\
                                        data[fields[1]].data[fields[2]]
                if len(fields) == 2:
                    if fields[1] == 'name':
                        bundle.data[fields[0]] = bundle.data[fields[0]].data[fields[1]]
                    else:
                        print bundle.data[fields[0]].data[fields[1]]
                        try:
                            bundle.data[fields[1]] = bundle.data[fields[0]].data[fields[1]]
                        except:
                            print 'skipping', fields

                #to_delete.append(fields[0])

        #for delete in to_delete:
        #    try:
        #        del bundle.data[delete]
        #    except:
        #        pass #already deleted

        """
        Saving the field names so we can create column names for tables later
        """
        for name, value in bundle.data.iteritems():
            try:
                if name not in self._meta.columns and name != 'id':
                    self._meta.columns.append(name)
            except:
                pass

        print 'return'
        return bundle


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




