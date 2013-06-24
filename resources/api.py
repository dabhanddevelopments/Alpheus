from tastypie.resources import Resource, ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
#from tastypie.authentication import SessionAuthentication
#from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from tastypie import fields
from app.models import * #Page, PageWindow, Window, Widget, WidgetType, Fund, FundType, Menu, Holding
from base_resources import MainBaseResource, TreeBaseResource
from django.http import HttpResponse

from tastypie.api import Api
api = Api(api_name="api")

class LoggedInResource(Resource):
    class Meta:
        pass

    def get_list(self, request, **kwargs):

        if request.user.is_authenticated():
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash


class WindowResource(MainBaseResource):
    pass

    class Meta(MainBaseResource.Meta):
        queryset = Window.objects.all()
        filtering = {
            'key': ALL,
        }


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
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=401)

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

class WidgetParamResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = WidgetParam.objects.all()


class WidgetsResource(MainBaseResource):
    widget_type = fields.ForeignKey(WidgetTypeResource, 'widget_type',full=True,)
    widget_param = fields.ToManyField(WidgetParamResource, 'widget_param',full=True,)
    window = fields.ForeignKey(WindowResource, 'window',full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Widget.objects.select_related('widget_type', 'widget_param').all()
        include_resource_uri = True
        exclude = ['description']

        filtering = {
            "window": ALL_WITH_RELATIONS,
        }


    def dehydrate(self, bundle):

        # @TODO: Consider getting rid of this
        bundle.data['type'] = bundle.data['widget_type'].data['key']

        qs = '?'
        params = {}
        for var in bundle.data['widget_param']:
            if var.data['value']:
                val = var.data['value']
            else:
                val = var.data['key'].upper()
            qs += str(var.data['key']) + '=' + str(val) + '&'
            
            params[var.data['key']] = var.data['value']

        bundle.data['qs'] = qs[:-1]
        #bundle.data['qs'] += bundle.data['columns'].replace(',', '&')
        bundle.data['params'] = params
        del bundle.data['widget_param']

        return bundle


    """
    def get_object_list(self, request):

        obj = super(WidgetsResource, self).get_object_list(request)

        # Limiting widgets by pre-defined user groups
        user_groups = [group.pk for group in request.user.groups.all()]
        return obj.filter(access__in=user_groups)

    """

class PageResource(TreeBaseResource, MainBaseResource):
    parent = fields.ForeignKey('self', 'parent', null=True, full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Page.objects.all().select_related('parent')
        allowed_methods = ['get']
        fields = ['id', 'title']
        filtering = {
            'parent': ALL,
        }

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


from base_resources import UserObjectsOnlyAuthorization
#curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"page": "/api/page/1/"", "widget": "/api/widget/1/"}' http://localhost:8000/api/pagewidget/
class PageWindowResource(MainBaseResource):
    user = fields.ForeignKey(UserResource, 'user', null=True)
    page = fields.ForeignKey(PageResource, 'page')
    window = fields.ForeignKey(WindowResource, 'window', full=True)

    class Meta(MainBaseResource.Meta):
        # what's this?
        authorization = UserObjectsOnlyAuthorization()
        queryset = PageWindow.objects.select_related('window').all()
        allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        always_return_data = True

        filtering = {
            "page": ALL_WITH_RELATIONS,
            "window": ALL_WITH_RELATIONS,
        }

    def apply_authorization_limits(self, request, object_list):

        qs = object_list.filter(user=request.user)

        # Use default config if user does not have their own yet
        if not qs:
            try:
                qs = object_list.filter(user=0)
            except:
                print 'no default page widget in db'
                #@TODO: log this

        return qs

    def dehydrate(self, bundle):
        #widget_type = bundle.data['widget'].data['widget_type'].data['key']
        #bundle.data['widget'].data['type'] = widget_type
        #del bundle.data['widget'].data['widget_type']
        return bundle

    def obj_create(self, bundle, **kwargs):

        # Add the user to the bundle
        return super(PageWindowResource, self).obj_create(
                                    bundle, user=bundle.request.user)


class FundTypeResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = FundType.objects.all()


class FundResourceAll(ModelResource):

    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        filtering = {
            "fund": ALL,
        }
api.register(FundResourceAll())


class FundResource(ModelResource):

    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        fields = ['id', 'name']
        filtering = {
            "fund": ALL,
        }
api.register(FundResource())

class FundByTypeResource(MainBaseResource):
    funds = fields.ToManyField(FundResource, "fund", full=True)

    class Meta(MainBaseResource.Meta):
        queryset = FundType.objects.all()

class FundNameResource(MainBaseResource):

    fund_type = fields.ForeignKey(FundTypeResource, "fund_type")

    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        fields = ['name', 'fund_type']

class MenuResource(TreeBaseResource, MainBaseResource):
    page = fields.ForeignKey(PageResource, "page", null=True, full=True)
    parent = fields.ForeignKey('self', 'parent', null=True)

    class Meta(MainBaseResource.Meta):
        queryset = Menu.objects.all().select_related('parent', 'page')
        allowed_methods = ['get']
        fields = ['id', 'name', 'page']

    def get_node_data(self, obj):

        try:
            page = obj.page.id
        except:
            page = 0

        try:
            fund = obj.fund.id
        except:
            fund = 0

        node = {
            'id': obj.id,
            'name': obj.name,
            'page': page,
            'fund': fund,
            'expanded': False
        }

        if obj.is_leaf_node():
            node['leaf'] = True
        else:
            node['children'] = [self.get_node_data(child) \
                                for child in obj.get_children()]
        return node


    def get_object_list(self, request):
        print request.user.is_authenticated()

        obj = super(MenuResource, self).get_object_list(request)

        # Limiting menus & tabs by pre-defined user groups
        #user_groups = [group.pk for group in request.user.groups.all()]
        #obj = obj.filter(access__in=user_groups)

        return obj

class MenuParentItemsResource(MainBaseResource):
    #page = fields.ForeignKey(PageResource, "page", null=True, full=True)
    parent = fields.ForeignKey('self', 'parent', null=True, full=True)

    class Meta(MainBaseResource.Meta):
        #queryset = Menu.objects.exclude(parent__isnull=False).select_related('parent')#, 'page')
        queryset = Menu.objects.all().select_related('parent')#, 'page')


class FundBenchResource(ModelResource):
    funds = fields.ToManyField(FundResource, 'funds')
    
    class Meta:
        queryset = FundBench.objects.all()
        filtering = {
            'funds': ALL,
        }

class CurrencyResource(ModelResource):
    
    class Meta:
        queryset = Currency.objects.all()

class CustodianResource(ModelResource):
    
    class Meta:
        queryset = Custodian.objects.all()

class AuditorResource(ModelResource):
    
    class Meta:
        queryset = Auditor.objects.all()

class AdministratorResource(ModelResource):
    
    class Meta:
        queryset = Administrator.objects.all()

class ClassificationResource(ModelResource):
    
    class Meta:
        queryset = Classification.objects.all()
        
class ManagerResource(ModelResource):
    
    class Meta:
        queryset = User.objects.all()

class HoldingCategoryResource(ModelResource):
    class Meta:
        queryset = HoldingCategory.objects.all()
        filtering = {
            'holding_group': ALL,
        }
        
class PurchaseSaleResource(ModelResource):

    class Meta:
        queryset = PurchaseSale.objects.all()
        

class HoldingResource(ModelResource):
    class Meta:
        queryset = Holding.objects.all()

class HoldingResourceFund(ModelResource):
    fund = fields.ForeignKey(FundResource, 'fund')   
    class Meta:
        queryset = Holding.objects.select_related('fund').all()
        filtering = {
            "fund": ALL,
        }           
        
class HoldingResourceDetail(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    currency = fields.ForeignKey(CurrencyResource, 'currency', full=True)
    sector = fields.ForeignKey(HoldingCategoryResource, 'sector', \
                                     related_name='sec', full=True)
    sub_sector = fields.ForeignKey(HoldingCategoryResource, 'sub_sector', \
                                        related_name='sub_sec', full=True)
    location = fields.ForeignKey(HoldingCategoryResource, 'location', \
                                    related_name='loc', full=True)
    

    class Meta:
        queryset = Holding.objects.all()
        filtering = {
            "fund": ALL_WITH_RELATIONS,
        }  
        
class ClientResource(ModelResource):
    
    class Meta(MainBaseResource.Meta):
        queryset = Client.objects.all()
        #filtering = {
        #    'fund': ALL,
        #}
# TODO: Move this to it's own file



api.register(UserResource())
api.register(WidgetsResource())
api.register(LoggedInResource())
api.register(MenuResource())
api.register(MenuParentItemsResource())
api.register(FundByTypeResource())
api.register(FundResource())
api.register(FundTypeResource(),canonical=True)
api.register(PageResource(),canonical=True)
api.register(PageWindowResource(),canonical=True)
api.register(HoldingResource())
api.register(HoldingResourceDetail())
