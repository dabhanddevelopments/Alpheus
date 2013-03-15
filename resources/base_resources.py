from tastypie.resources import Resource, ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from alpheus.serializers import PrettyJSONSerializer

# Base Model Resource
class MainBaseResource(ModelResource):
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


