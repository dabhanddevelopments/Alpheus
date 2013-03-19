from tastypie.resources import Resource, ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
#from tastypie.authentication import SessionAuthentication
#from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from tastypie import fields
from app.models import Page, PageWidget, Widget, WidgetType, Fund, FundType, Menu
from base_resources import MainBaseResource, TreeBaseResource
from widgets import InfoResource

class LoggedInResource(Resource):
    class Meta:
        pass

    def get_list(self, request, **kwargs):

        from django.http import HttpResponse

        if request.user.is_authenticated():
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


"""
# remove later
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from app.models import Entry




class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

# end remove later
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash


#curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"username" : "me", "password": "l33t"}' http://localhost:8003/api/user/login/

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        resource_name = 'user'

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        #data = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)



# only used internally
class WidgetTypeResource(MainBaseResource):

    class Meta:
        queryset = WidgetType.objects.all()
        include_resource_uri = False


class WidgetResource(MainBaseResource):
    widget_type = fields.ForeignKey(WidgetTypeResource, 'widget_type',full=True,)

    class Meta(MainBaseResource.Meta):
        queryset = Widget.objects.select_related('widget_type').all()
        include_resource_uri = True

    def dehydrate(self, bundle):

        # @TODO: Consider getting rid of this
        bundle.data['type'] = bundle.data['widget_type'].data['key']

        # Description is only used for UnusedWidgetResource
        del bundle.data['description']

        return bundle


    def get_object_list(self, request):

        obj = super(WidgetResource, self).get_object_list(request)

        # Limiting widgets by pre-defined user groups
        user_groups = [group.pk for group in request.user.groups.all()]
        return obj.filter(access__in=user_groups)


class PageResource(TreeBaseResource, MainBaseResource):
    parent = fields.ForeignKey('self', 'parent', null=True, full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Page.objects.all().select_related('parent')
        allowed_methods = ['get']
        fields = ['id', 'title']

    # Controls the data structure of the output
    def get_node_data(self, obj):
        node = {
            'id': obj.id,
            'title': obj.title
        }
        
        if not obj.is_leaf_node():
            node['children'] = [self.get_node_data(child) \
                                for child in obj.get_children()]
        return node


from tastypie.authentication import SessionAuthentication
from base_resources import UserObjectsOnlyAuthorization
from alpheus.serializers import PrettyJSONSerializer
#curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"page": "/api/page/1/"", "widget": "/api/widget/1/"}' http://localhost:8000/api/pagewidget/
class PageWidgetResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True)
    page = fields.ForeignKey(PageResource, 'page')
    widget = fields.ForeignKey(InfoResource, 'widget',full=True,)

    class Meta:
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        serializer = PrettyJSONSerializer()
        include_resource_uri = False
        queryset = PageWidget.objects.select_related(
            'grid', 'widget', 'widget__widget_type').all()
        allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        always_return_data = True

        filtering = {
            "page": ALL_WITH_RELATIONS,
        }

    def apply_authorization_limits(self, request, object_list):

        print 'applying auth limits'

        qs = object_list.filter(user=request.user)

        print qs

        # Use default config if user does not have their own yet
        if not qs:
            try:
                qs = object_list.filter(user=0)
            except:
                print 'no default page widget in db'
                #@TODO: log this

        return qs

    def dehydrate(self, bundle):
        widget_type = bundle.data['widget'].data['widget_type'].data['key']
        bundle.data['widget'].data['type'] = widget_type
        del bundle.data['widget'].data['widget_type']
        return bundle

    def obj_create(self, bundle, **kwargs):

        # Add the user to the bundle, why?
        return super(PageWidgetResource, self).obj_create(
                                    bundle, user=bundle.request.user)
 


class FundTypeFundsResource(MainBaseResource):
    fund = fields.ToManyField('app.api.FundResource', 'fund', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = FundType.objects.all()


class FundTypeResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = FundType.objects.all()


# only used internally
class FundResource(ModelResource):

    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        fields = ['id', 'name']

class FundNameResource(MainBaseResource):

    fund_type = fields.ForeignKey(FundTypeResource, "fund_type")

    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        fields = ['name', 'fund_type']



class MenuResource(TreeBaseResource, MainBaseResource):
    page = fields.ForeignKey(PageResource, "page", null=True)
    parent = fields.ForeignKey('self', 'parent', null=True)

    class Meta(MainBaseResource.Meta):
        queryset = Menu.objects.all().select_related('parent', 'page')
        allowed_methods = ['get']
        fields = ['id', 'name', 'page']

    def get_node_data(self, obj):
        node = {
            'id': obj.id,
            'name': obj.name,
            'page': obj.page,
            'expanded': False
        }

        if obj.is_leaf_node():
            node['leaf'] = True
        else:
            node['children'] = [self.get_node_data(child) \
                                for child in obj.get_children()]
        return node


    def get_object_list(self, request):

        obj = super(MenuResource, self).get_object_list(request)

        """
        Limiting menus by pre-defined user groups
        """
        user_groups = [group.pk for group in request.user.groups.all()]
        return obj.filter(access__in=user_groups).distinct()


class MenuParentItemsResource(MainBaseResource):
    #page = fields.ForeignKey(PageResource, "page", null=True, full=True)
    parent = fields.ForeignKey('self', 'parent', null=True, full=True)

    class Meta(MainBaseResource.Meta):
        #queryset = Menu.objects.exclude(parent__isnull=False).select_related('parent')#, 'page')
        queryset = Menu.objects.all().select_related('parent')#, 'page')


# TODO: Move this to it's own file
from tastypie.api import Api

api = Api(api_name="api")
api.register(UserResource())
api.register(LoggedInResource())
api.register(MenuResource())
api.register(MenuParentItemsResource())
api.register(FundTypeFundsResource())
api.register(FundResource())
api.register(FundTypeResource(),canonical=True)
api.register(PageResource(),canonical=True)
api.register(PageWidgetResource(),canonical=True)
