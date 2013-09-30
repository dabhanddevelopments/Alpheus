# myapp/api/resources.py
from tastypie import fields
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from alpheus.serializers import PrettyJSONSerializer
from tastypie.api import Api
from django.contrib.auth.models import User

from alpheus.base_resources import MainBaseResource, TreeBaseResource, StandardBaseResource
from app.models import *
from holding.models import *
from fund.models import *
from client.models import *
from comparative.models import *

import random
from datetime import datetime, date
from django.http import HttpResponse



class LoggedInResource(Resource):
    class Meta:
        pass

    def get_list(self, request, **kwargs):

        from django.http import HttpResponse

        if request.user.is_authenticated():
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash


class WindowResource(StandardBaseResource):
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
class WidgetTypeResource(StandardBaseResource):

    class Meta:
        queryset = WidgetType.objects.all()
        include_resource_uri = False

class WidgetParamResource(StandardBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = WidgetParam.objects.all()


class WidgetsResource(StandardBaseResource):
    widget_type = fields.ForeignKey(WidgetTypeResource, 'widget_type',full=True,)
    widget_param = fields.ToManyField(WidgetParamResource, 'widget_param',full=True,)
    window = fields.ForeignKey(WindowResource, 'window',full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Widget.objects.select_related('widget_type', 'widget_param').all()
        include_resource_uri = True
        exclude = ['description']

        filtering = {
            "window": ALL_WITH_RELATIONS,
            "enabled": ALL,
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

class PageResource(TreeBaseResource, StandardBaseResource):
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


from alpheus.base_resources import UserObjectsOnlyAuthorization
#curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"page": "/api/page/1/"", "widget": "/api/widget/1/"}' http://localhost:8000/api/pagewidget/
class PageWindowResource(StandardBaseResource):
    user = fields.ForeignKey(UserResource, 'user', null=True)
    page = fields.ForeignKey(PageResource, 'page')
    window = fields.ForeignKey(WindowResource, 'window', full=True)

    class Meta(MainBaseResource.Meta):
        # what's this?
        authorization = UserObjectsOnlyAuthorization()
        queryset = PageWindow.objects.select_related('window').all()
        #allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        always_return_data = True

        filtering = {
            "page": ALL_WITH_RELATIONS,
            "window": ALL_WITH_RELATIONS,
        }

    def apply_authorization_limits2(self, request, object_list):

        qs = object_list.filter(user=request.user)

        # Use default config if user does not have their own yet
        if not qs:
            try:
                qs = object_list.filter(user=0)
            except:
                print 'no default page widget in db'
                #@TODO: log this

        return qs

    def dehydrate2(self, bundle):
        #widget_type = bundle.data['widget'].data['widget_type'].data['key']
        #bundle.data['widget'].data['type'] = widget_type
        #del bundle.data['widget'].data['widget_type']
        return bundle

    def obj_create2(self, bundle, **kwargs):

        # Add the user to the bundle
        return super(PageWindowResource, self).obj_create(
                                    bundle, user=bundle.request.user)



class CustodianResource(MainBaseResource):

    class Meta:
        queryset = Custodian.objects.all()
        filtering = {
            'key': ALL,
        }


class AuditorResource(MainBaseResource):

    class Meta:
        queryset = Auditor.objects.all()

class AdministratorResource(MainBaseResource):

    class Meta:
        queryset = Administrator.objects.all()

class ClassificationResource(MainBaseResource):

    class Meta:
        queryset = Classification.objects.all()

class ManagerResource(MainBaseResource):

    class Meta:
        queryset = User.objects.all()

"""
class FundClassificationResource(MainBaseResource):
    classification = fields.ForeignKey(ClassificationResource, "classification")
    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.select_related('classification')
        fields = ['id', 'name', 'classification__name']
        filtering = {
            "fund": ALL,
        }
api.register(FundClassificationResource())
"""



class MenuResource(TreeBaseResource, StandardBaseResource):
    page = fields.ForeignKey(PageResource, "page", null=True, full=True)
    parent = fields.ForeignKey('self', 'parent', null=True)

    class Meta(MainBaseResource.Meta):
        queryset = Menu.objects.all().select_related('parent', 'page', 'fund')
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

        obj = super(MenuResource, self).get_object_list(request)

        # Limiting menus & tabs by pre-defined user groups
        user_groups = [group.pk for group in request.user.groups.all()]
        obj = obj.filter(access__in=user_groups).distinct()

        return obj

class MenuParentItemsResource(StandardBaseResource):
    #page = fields.ForeignKey(PageResource, "page", null=True, full=True)
    parent = fields.ForeignKey('self', 'parent', null=True, full=True)

    class Meta(MainBaseResource.Meta):
        #queryset = Menu.objects.exclude(parent__isnull=False).select_related('parent')#, 'page')
        queryset = Menu.objects.all().select_related('parent')#, 'page')



class CurrencyResource(StandardBaseResource):

    class Meta:
        queryset = Currency.objects.all()

# not used atm
class WidgetBaseResource(StandardBaseResource):

    """
    Base class for all widgets
    * Filters out all widgets the user does not have access to
    """
    class Meta:
        queryset = Widget.objects.all()

    def get_object_list(self, request):

        obj = super(WidgetBaseResource, self).get_object_list(request)
        return obj

        """
        Limiting widgets by pre-defined user groups
        """
        user_groups = [group.pk for group in request.user.groups.all()]
        return obj.filter(access__in=user_groups).distinct()

# Only used internally
class TypeResource(StandardBaseResource):

    class Meta:
        queryset = WidgetType.objects.all()
        include_resource_uri = False


class InfoResource(WidgetBaseResource):

    """
    Returns widget & widget type details
    """

    widget_type = fields.ForeignKey(TypeResource, 'widget_type',full=True,)

    class Meta(WidgetBaseResource.Meta):
        queryset = Widget.objects.select_related('widget_type').all()
        resource_name = 'widget-info'
        include_resource_uri = True

    def dehydrate(self, bundle):

        # @TODO: Consider getting rid of this
        bundle.data['type'] = bundle.data['widget_type'].data['key']

        return bundle


# not used atm (ironically)
class UnusedResource(WidgetBaseResource):

    """
    Returns unused widgets on the specified page
    """

    widget_type = fields.ForeignKey(TypeResource, 'widget_type',full=True)

    class Meta(WidgetBaseResource.Meta):
        resource_name = 'widget-unused'
        filtering = {
            "page": ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data['widget_type'] = bundle.data['widget_type'].data['name']
        return bundle

    def get_object_list(self, request):

        obj = super(UnusedResource, self).get_object_list(request)

        # Filter out all the existing widgets on this Page
        existing_widgets = PageWindow.objects \
                .values_list('widget__id', flat=True) \
                .filter(user=request.user, page=request.REQUEST.get('page'))

        qs = obj.exclude(id__in=existing_widgets).select_related('widget_type')

        return qs


class DuplicateResource(StandardBaseResource):
    class Meta:
        queryset = Window.objects.all()

    def get_object_list(self, request):

        objects = super(SpecifiedFields, self).get_object_list(request)

        for obj in objects:
            obj.name

class ImportResource(StandardBaseResource):

    class Meta:
        queryset = Fund.objects.all()
        authorization = DjangoAuthorization()

    def rand_str(self, size = 8):
        import string


        allowed = string.ascii_letters # add any other allowed characters here
        allowed2 = allowed[random.randint(0, len(allowed) - 1)]
        randomstring = ''.join([allowed2 for x in xrange(size)])
        return randomstring


    def get_field_data(self, obj):
        fields = obj._meta.fields
        field_data = {}
        for field in fields:
            if field.get_internal_type() == 'DecimalField':
                field_data[field.name] = random.randrange(0, 2000)
        return field_data

    def alter_list_data_to_serialize(self, request, data):

        def rand_date():
            return str(random.randrange(year_start, year_end)) + '-' + \
                    str(random.randrange(month_start, month_end)) + '-' + \
                                                str(random.randrange(1, 28))

        year_start = 2010
        year_end = 2014
        month_start = 1
        month_end = 13
        day_start = 1
        day_end = 32
        no_of_trades = 100


        currency = Currency.objects.all()
        counter_party = CounterParty.objects.all()


        fee = Fee.objects.all()

        country = Country.objects.all()

        alarm = Alarm(name="alarm1").save()
        alarm = Alarm.objects.all() # is this needed?

        administrator = Administrator.objects.all()
        auditor = Auditor.objects.all()
        classification = Classification.objects.all()
        user = User.objects.all()
        custodian = Custodian.objects.all()

        # FxRate
        for year in range(year_start, year_end):
            for month in range(month_start, month_end):
                for day in range(day_start, day_end):
                    for cur in currency:

                        try:
                            fxrate = FxRate(
                                value_date = date(year, month, day),
                                currency = cur,
                                fx_rate = random.randrange(1, 2),
                            )
                            fxrate.save()
                        except:
                            pass

        # Fund classifications
        classification_names = [
            'Fund (Fund of Fund)',
            'Fixed Income & Treasuries Gale G',
            'Fixed Income & Treasuries CS Fixed Income',
            'Equities, Options, Futures Gale L, M, N',
            'Equities, Options, Futures CS Equities', #5
            'Equities, Options, Futures CS Cal/Vol',
            'Equities, Options, Futures CS Options',
            'Limited Holdings',
            'Side Pockets',
            'Private Equity', #10
            'Alpheus',
        ]
        classifications = [Classification(name=name) for name in classification_names]
        class_data = []
        for id, name in enumerate(classification_names):
            class_data.append(Classification(
                #key = id,
                name = name,
                asset_class = Category.objects.order_by('?')[0]
            ))
        Classification.objects.bulk_create(class_data, batch_size=100)
        #classifications = Classification.objects.all()

        # Fund
        fund_names = {
            'Gale B': 1, 'Gale E': 1, 'Gale G': 2,
            'Gale H': 8, 'Gale I': 8, 'Gale K': 9,
            'Gale L': 4, 'Gale M': 4, 'Gale N': 4,
            'CS European Equity': 5, 'CS US Equity': 5,
            'CS Asia Equity': 5, 'CS Volaility': 6,
            'CS Fixed Income & Treasuries': 3, 'CS Options': 7,
            'Private Equity': 10,
            'Alpheus': 11,
        }

        #from fund.models import Classification as FundClassification

        data = []
        for name, classification in fund_names.iteritems():
            if name[0:1] == 'CS':
                cp = counter_party[1]
            else:
                cp = counter_party[0]

            fields = self.get_field_data(Fund)
            fields['name'] = name
            fields['subscription_frequency'] = 'm'
            fields['redemption_frequency'] = 'm'
            #fields['counter_party'] = cp
            fields['currency'] = Currency.objects.order_by('?')[0]
            fields['alarm'] = Alarm.objects.order_by('?')[0]
            fields['custodian'] = Custodian.objects.order_by('?')[0]
            fields['auditor'] = Auditor.objects.order_by('?')[0]
            fields['administrator'] = Administrator.objects.order_by('?')[0]
            fields['classification'] = Classification.objects.get(pk=classification)
            fields['user'] = User.objects.order_by('?')[0]
            #fields['classification'] = classifications.get(pk=classification)
            fields['value_date'] = '2013-07-10' #whatever current date
            data.append(Fund(**fields))

        Fund.objects.bulk_create(data, batch_size=100)

        # Fund History
        funds = Fund.objects.all()
        data = []
        for fund in funds:
            for year in range(year_start, year_end):
                for month in range(month_start, month_end):

                    fields = self.get_field_data(FundHistory)
                    fields['fund'] = fund
                    fields['date_type'] = 'm'
                    fields['value_date'] = date(year, month, 1)
                    data.append(FundHistory(**fields))
                    for day in range(day_start, day_end):

                        # skip weekends
                        try:
                            if date(year, month, day).weekday() > 4:
                                continue
                        except:
                            continue

                        fields = self.get_field_data(FundHistory)
                        fields['fund'] = fund
                        fields['date_type'] = 'd'
                        fields['value_date'] = date(year, month, day)
                        data.append(FundHistory(**fields))

        FundHistory.objects.bulk_create(data, batch_size=100)

        # Benchmarks
        benchmark_names = ['IBEX - 50', 'EUROSTOXX 500', 'FTSE 100']
        data = []
        for name in benchmark_names:
            fields = self.get_field_data(Benchmark)
            fields['name'] = name
            fields['benchmark_type'] = 'bloomberg'
            fields['value_date'] = '2013-07-10' #whatever current date
            data.append(Benchmark(**fields))

        Benchmark.objects.bulk_create(data)

        # Benchmark History
        benchmarks = Benchmark.objects.all()
        data = []
        for benchmark in benchmarks:
            for year in range(year_start, year_end):
                for month in range(month_start, month_end):
                    fields = self.get_field_data(Benchmark)
                    fields['benchmark'] = benchmark
                    fields['date_type'] = 'm'
                    fields['value_date'] = date(year, month, 1)
                    data.append(BenchmarkHistory(**fields))
                    for day in range(day_start, day_end):

                        # skip weekends
                        try:
                            if date(year, month, day).weekday() > 4:
                                continue
                        except:
                            continue

                        fields = self.get_field_data(Benchmark)
                        fields['benchmark'] = benchmark
                        fields['date_type'] = 'd'
                        fields['value_date'] = date(year, month, day)
                        data.append(BenchmarkHistory(**fields))

        BenchmarkHistory.objects.bulk_create(data, batch_size=100)
        benchmark = Benchmark.objects.all()


        # Client
        client_names = [
            ['Tianna', 'Toft'],
            ['Jeanette', 'Jeon'],
            ['Chantay', 'Cogan'],
            ['Janene', 'Jonason'],
            ['Lissette', 'Loveland'],
            ['Ludivina', 'Lanz'],
            ['Randa', 'Riggleman'],
            ['Arturo', 'Andrea'],
            ['Lucienne', 'Lis'],
            ['Meri', 'Majors'],
            ['Christian', 'Coney'],
            ['Ramonita', 'Ruffino'],
            ['Trudie', 'Terrill'],
            ['Don', 'Duplessis'],
            ['Caprice', 'Crosswell'],
            ['Kisha', 'Krejci'],
            ['Cathi', 'Capito'],
            ['Maxie', 'Maiorano'],
            ['Dede', 'Dahlquist'],
            ['Byron', 'Blossom'],
            ['Booker', 'Brayboy'],
            ['Henry', 'Hajek'],
            ['Belen', 'Bazan'],
            ['Rina', 'Rasnick'],
            ['Lorinda', 'Leis'],
            ['Destiny', 'Dowe'],
            ['Tonda', 'Trybus'],
            ['Rachell', 'Rentschler'],
            ['Stefanie', 'Sorrells'],
            ['Clayton', 'Cabello'],
            ['Kimberli', 'Kincheloe'],
            ['Louis', 'Litwin'],
            ['Selena', 'Shaw'],
            ['Carlota', 'Confer'],
            ['Adena', 'April'],
            ['Rosaria', 'Rousselle'],
            ['Anjanette', 'Alsop'],
            ['Margert', 'Mcclenton'],
            ['Delphine', 'Delp'],
            ['Lizzie', 'Leos'],
            ['Marinda', 'Mccowen'],
            ['Tommye', 'Thames'],
            ['Velva', 'Villagrana'],
            ['Noel', 'Nicoll'],
            ['Magen', 'Mcentire'],
            ['Chantel', 'Chiaramonte'],
            ['Julene', 'Jahn'],
            ['Erik', 'Elza'],
            ['Charlesetta', 'Cowie'],
            ['Janel', 'Jurgens'],
            ['Indira', 'Islam'],
            ['Horace', 'Haberle'],
            ['Adrien', 'Abe'],
            ['Ellena', 'Eanes'],
            ['Temeka', 'Testa'],
            ['Daisy', 'Dancy'],
            ['Darell', 'Driggs'],
            ['Georgette', 'Gooslin'],
            ['Daryl', 'Driggers'],
            ['June', 'Judge'],
            ['Sidney', 'Scheetz'],
            ['Alishia', 'Arab'],
            ['Christen', 'Caffrey'],
            ['Jeffery', 'Jinks'],
            ['Klara', 'Kimbell'],
            ['Era', 'Ehrmann'],
            ['Zoraida', 'Zehr'],
            ['Melda', 'Morlan'],
            ['Noelia', 'Norsworthy'],
            ['Elwanda', 'Eaddy'],
            ['Madie', 'Mintz'],
            ['Annelle', 'Auger'],
            ['Katelin', 'Kehl'],
            ['Akilah', 'Augusta'],
            ['Kimberli', 'Kramp'],
            ['Tandra', 'Triolo'],
            ['Eilene', 'Empson'],
            ['Merrilee', 'Mechem'],
            ['Annette', 'Ahern'],
            ['Denese', 'Devito'],
            ['Keven', 'Kimsey'],
            ['Sheldon', 'Steck'],
            ['Saturnina', 'Setton'],
            ['Murray', 'Mcgavock'],
            ['Treena', 'Troutt'],
            ['Valery', 'Vero'],
            ['Arnetta', 'Alberts'],
            ['Shaun', 'Sorge'],
            ['Alena', 'Aquino'],
            ['Adelaide', 'Avant'],
            ['Jama', 'Jiles'],
            ['Nicholle', 'Nickell'],
            ['Alma', 'Ahlgren'],
            ['Nichole', 'Newborn'],
            ['Courtney', 'Coldwell'],
            ['Rubi', 'Rossiter'],
            ['Will', 'Wasden'],
            ['Coleen', 'Corbitt'],
            ['Nova', 'Neel'],
            ['Israel', 'Ingerson'],
        ]
        data = []
        for name in client_names:
            fields = self.get_field_data(Client)
            fields['first_name'] = name[0]
            fields['last_name'] = name[1]
            fields['value_date'] = '2013-07-10' #whatever current date
            data.append(Client(**fields))

        Client.objects.bulk_create(data, batch_size=100)


        # Subscription Redemption
        funds = Fund.objects.all()
        clients = Client.objects.all()
        data = []
        for fund in funds:
            for client in clients:

                # do not assign every client to every fund
                if not random.randrange(0, 2):
                    fields = self.get_field_data(SubscriptionRedemption)
                    fields['client'] = client
                    fields['fund'] = fund
                    fields['trade_date'] = rand_date()
                    #fields['input_date'] = rand_date()
                    fields['settlement_date'] = rand_date()
                    fields['redemption_date'] = rand_date()
                    fields['full_redemption'] = 1
                    fields['instruction_type'] = 'new'
                    fields['sub_red_switch'] = random.randrange(0, 5)
                    fields['percent_released'] = 90
                    data.append(SubscriptionRedemption(**fields))

        SubscriptionRedemption.objects.bulk_create(data, batch_size=100)
        client = Client.objects.all()



        # Client History
        data = []
        for client in clients:

            # limit client history, otherwise it would take too long
            if client.last_name[0].lower() == 'c':

                for year in range(year_start, year_end):
                    for month in range(month_start, month_end):
                        fields = self.get_field_data(Client)
                        fields['client'] = client
                        fields['value_date'] = date(year, month, 1)
                        fields['date_type'] = 'm'
                        data.append(ClientHistory(**fields))
                        for day in range(day_start, day_end):

                            # skip weekends
                            try:
                                if date(year, month, day).weekday() > 4:
                                    continue
                            except:
                                continue

                            fields = self.get_field_data(Client)
                            fields['client'] = client
                            fields['date_type'] = 'd'
                            fields['value_date'] = date(year, month, day)
                            data.append(ClientHistory(**fields))

                # blatant copy & paste
                for year in range(year_start, year_end):
                    for month in range(month_start, month_end):
                        fields = self.get_field_data(Client)
                        fields['client'] = client
                        fields['value_date'] = date(year, month, 1)
                        fields['date_type'] = 'm'
                        data.append(ClientHistory(**fields))
                        for day in range(day_start, day_end):

                            # skip weekends
                            try:
                                if date(year, month, day).weekday() > 4:
                                    continue
                            except:
                                continue

                            fields = self.get_field_data(Client)
                            fields['client'] = client
                            fields['date_type'] = 'd'
                            fields['value_date'] = date(year, month, day)
                            data.append(ClientHistory(**fields))


        ClientHistory.objects.bulk_create(data, batch_size=100)





        classification_names = ['CS Funds', 'Gale Funds', 'PE commitments', 'Ad-hoc', 'Loans', 'Cash' ]

        fund_lis = [fund_name for fund_name, classification in fund_names.iteritems()]
        # Holding
        holding_names = ['Coca Cola', 'Pepsi', 'Pussy'] + fund_lis
        data = []
        for holding_name in holding_names:
            fields = self.get_field_data(Holding)
            fields['name'] = holding_name
            fields['currency'] = Currency.objects.order_by('?')[0]
            fields['country'] = Country.objects.order_by('?')[0]
            fields['counter_party'] = CounterParty.objects.order_by('?')[0]
            fields['sector'] = Category.objects.filter(group='sec').order_by('?')[0]
            fields['sub_sector'] = Category.objects.filter(group='sub').order_by('?')[0]
            fields['location'] = Category.objects.filter(group='loc').order_by('?')[0]
            fields['investment_type'] = Category.objects.filter(group='inv').order_by('?')[0]
            fields['asset_class'] = Category.objects.filter(group='ass').order_by('?')[0]
            fields['sec_id'] = self.rand_str()
            fields['bloomberg_code'] = self.rand_str()
            fields['isin'] = self.rand_str()
            fields['rep_code'] = self.rand_str()
            fields['description'] = self.rand_str(100)
            fields['valoren'] = random.randrange(0, 10)
            fields['redemption_frequency'] = random.randrange(0, 4)
            fields['redemption_date'] = rand_date()
            fields['value_date'] = rand_date()
            fields['dealing_date'] = rand_date()
            fields['soft_lock_date'] = rand_date()
            fields['maturity'] = rand_date()
            fields['put_call'] = 1
            fields['american_euro'] = 1
            fields['etf_yes_no'] = 1
            data.append(Holding(**fields))

        Holding.objects.bulk_create(data, batch_size=100)

        # Holding History
        data = []
        for holding in Holding.objects.all():
            for year in range(year_start, year_end):
                for month in range(month_start, month_end):
                    fields = self.get_field_data(HoldingHistory)
                    fields['holding'] = holding
                    fields['date_type'] = 'm'
                    fields['value_date'] = date(year, month, 1)
                    #fields['redemption_date'] = rand_date()
                    fields['dealing_date'] = rand_date()
                    fields['date_type'] = 'm'
                    data.append(HoldingHistory(**fields))
                    for day in range(day_start, day_end):

                        # skip weekends
                        try:
                            if date(year, month, day).weekday() > 4:
                                continue
                        except:
                            continue

                        fields = self.get_field_data(HoldingHistory)
                        fields['holding'] = holding
                        fields['date_type'] = 'd'
                        fields['value_date'] = date(year, month, day)
                        fields['dealing_date'] = rand_date()
                        data.append(HoldingHistory(**fields))

        HoldingHistory.objects.bulk_create(data, batch_size=100)

        cpt = CounterPartyTrader(name='John Doe')
        cpt.save()

        from trade.models import Trade

        # Trade
        data = []
        for index in range(1, no_of_trades):

            fields = self.get_field_data(Trade)
            fields['counter_party'] = CounterParty.objects.order_by('?')[0]
            fields['counter_party_trader'] = CounterPartyTrader.objects.order_by('?')[0]
            fields['authorised_by'] = User.objects.order_by('?')[0]
            fields['desk'] = self.rand_str()
            fields['book'] = self.rand_str()
            fields['bank_reference'] = self.rand_str()
            fields['memorandum_text'] = self.rand_str()
            fields['holding'] = Holding.objects.order_by('?')[0]
            #fields['trade_type'] = TradeType.objects.order_by('?')[0]
            #fields['currency'] = Currency.objects.order_by('?')[0]
            #fields['purchase_price_base'] = random.randrange(50,125)
            fields['base_nav'] = random.randrange(50,125)
            fields['settlement_date'] = rand_date()
            fields['trade_date'] = rand_date()
            fields['buy_sell'] = 1
            fields['to_open_to_close'] = 1
            data.append(Trade(**fields))

        Trade.objects.bulk_create(data, batch_size=100)


        # CurrencyPosition
        data = []
        funds = Fund.objects.all()
        currencies = Currency.objects.all()
        for fund in funds:
            for currency in currencies:
                for year in range(year_start, year_end):
                    for month in range(month_start, month_end):
                        for day in range(day_start, day_end):

                            # skip weekends
                            try:
                                if date(year, month, day).weekday() > 4:
                                    continue
                            except:
                                continue

                            fields = self.get_field_data(CurrencyPosition)
                            fields['fund'] = fund
                            fields['currency'] = currency
                            fields['value_date'] = date(year, month, day)
                            data.append(CurrencyPosition(**fields))

        CurrencyPosition.objects.bulk_create(data, batch_size=100)

        # Breakdown
        holding_categories = Category.objects.all()
        data = []
        data_cb = []
        for fund in funds:
            for cat in holding_categories:
                for year in range(year_start, year_end):
                    for month in range(month_start, month_end):
                        #for day in range(day_start, day_end):

                        # skip weekends
                        #try:
                        #    if date(year, month, day).weekday() > 4:
                        #        continue
                        #except:
                        #    continue

                        fields = self.get_field_data(Breakdown)
                        fields['fund'] = fund
                        fields['category'] = cat
                        fields['value_date'] = date(year, month, 1)
                        data.append(Breakdown(**fields))


                        # Country Breakdown
                        if cat.group == 'loc':

                            if cat.name == 'Latin America':
                                countries = ['Brazil', 'Mexico', 'Chile', 'Peru']
                            elif cat.name == 'EM':
                                countries = ['U.K', 'Spain', 'Greece']
                            elif cat.name == 'Asia':
                                countries = ['Singapore', 'China', 'Japan']
                            else:
                                countries = False

                            if countries:
                                for country in countries:
                                    fields = self.get_field_data(CountryBreakdown)
                                    fields['fund'] = fund
                                    fields['country'] = Country.objects.get(name=country)
                                    fields['category'] = cat
                                    fields['value_date'] = date(year, month, 1)
                                    data_cb.append(CountryBreakdown(**fields))

        Breakdown.objects.bulk_create(data, batch_size=100)
        CountryBreakdown.objects.bulk_create(data_cb, batch_size=100)
        return {'done'}

