from tastypie.resources import Resource, ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from app.models import *
from resources.api import FundResource, HoldingResource
from resources.base_resources import MainBaseResource
#from app import widget_models
from alpheus.serializers import PrettyJSONSerializer
from django.db.models import Avg
import datetime 
from time import mktime

from tastypie.api import Api
from tastypie.paginator import Paginator
from django.http import HttpResponse
import json
import calendar
import datetime
#from datetime import date
#from datetime import timedelta
from alpheus.utils import JsonResponse
from alpheus import settings

class WidgetBaseResource(MainBaseResource):

    """
    Base class for all widgets
    * Filters out all widgets the user does not have access to
    """
    class Meta(MainBaseResource.Meta):
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
class TypeResource(ModelResource):

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
        include_resource_uri = True
        allowed_methods = ['get', 'post', 'put', 'delete']

    def dehydrate(self, bundle):

        # @TODO: Consider getting rid of this
        bundle.data['type'] = bundle.data['widget_type'].data['key']

        return bundle


class UnusedResource(WidgetBaseResource):

    """
    Returns unused widgets on the specified page
    """

    widget_type = fields.ForeignKey(TypeResource, 'widget_type',full=True,)

    class Meta(WidgetBaseResource.Meta):

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



class Graph(WidgetBaseResource):
    class Meta:
        queryset = Widget.objects.all()
        serializer = PrettyJSONSerializer()
        include_resource_uri = False

    def dehydrate(self, bundle):
        #result = getattr(widget_models, 'concern_occurrance')(bundle)
        return [[1, 2],[3,5.12],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]

class ConcernOccurrance(WidgetBaseResource):
    class Meta:
        queryset = Widget.objects.all()
        serializer = PrettyJSONSerializer()

    def dehydrate(self, bundle):
        return [['HSBC', 7], ['Credit Suisse', 9], ['Private Equity', 18], ['Other', 3]]

class ExampleTable1(WidgetBaseResource):
    class Meta:
        queryset = Widget.objects.all()
        serializer = PrettyJSONSerializer()

    def dehydrate(self, bundle):
        return [
            { 'name': 'Lisa',  "email":"lisa@simpsons.com",  "phone":"555-111-1224"  },
            { 'name': 'Bart',  "email":"bart@simpusons.com",  "phone":"555-222-1234" },
            { 'name': 'Homer', "email":"home@simpsons.com",  "phone":"555-222-1244"  },
            { 'name': 'Marge', "email":"marge@simpsons.com", "phone":"555-222-1254"  }
        ]


class PieChart(WidgetBaseResource):
    class Meta:
        queryset = Widget.objects.all()
        serializer = PrettyJSONSerializer()
        include_resource_uri = False

    def dehydrate(self, bundle):
        return [['HSBC', 7], ['Credit Suisse', 9], ['Private Equity', 18], ['Other', 3]]











class FundGroupPerfResource2(MainBaseResource):
    
    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.all()

        filtering = {
            "identifier": ALL_WITH_RELATIONS,
        }





class CurrencyResource(ModelResource):
    
    class Meta:
        queryset = Currency.objects.all()
        
class TradeTableResource(MainBaseResource):
    #holding = fields.ForeignKey(HoldingResource, 'holding', null=True)
    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.all()
        fields = [
            'identifier', 'trade_date', 'settlement_date', 'purchase_sale',
            'no_of_units', 'purchase_price', 'fx_euro', 
        ]
        filtering = {
            "identifier": ALL_WITH_RELATIONS,
        }
        
    def alter_list_data_to_serialize(self, request, data):
    
        fields = self._meta.fields
        for x in fields:
            if x == 'identifier':
                fields.remove(x)  
        columns = self.set_columns(self._meta.fields, [80, 80])

        dic = {
            'metaData': {'sorting': 'name'},
            'columns': columns,
            'rows': data,
        }
        return dic
          

class TradeBarGraphResource(TradeTableResource):

    class Meta(TradeTableResource.Meta):
        pass
         

    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))
            
        lis = []        
        for row in objects:                
            date = int(mktime(row.trade_date.timetuple())) * 1000
            innerlis=[int(str(date)), row.no_of_units]
            lis.append(innerlis)
        return JsonResponse(lis)
  
class FundBenchResource(MainBaseResource):
    funds = fields.ManyToManyField(Fund, 'funds')
        
    class Meta:
        queryset = FundBench.objects.all()
        filtering = {
            'funds': ALL,
        }

"""
could not get this to work.

class FundBenchResource(MainBaseResource):
    entries = fields.ToManyField('resources.widgets.FundBenchHistResource', 'history', related_name='benchmark', full=True )
    class Meta:
        queryset = FundBench.objects.all()
        resource_name = 'benchmark' 
class FundBenchHistResource(MainBaseResource):
    user = fields.ForeignKey(FundBenchResource, 'benchmark', related_name='history')    
"""
        
class FundBenchDataTableResource(MainBaseResource):

    funds = fields.ManyToManyField(FundResource, 'funds')
    
    class Meta(MainBaseResource.Meta):
        queryset = FundBench.objects.all()
        filtering = {
            "funds": ALL,
        }

    # fund param is mandatory
    def build_filters(self, filters=None):
        self.check_params(['funds'], filters)
        return super(FundBenchDataTableResource, self).build_filters(filters)
        
    def get_list(self, request, **kwargs):
    
        base_bundle = self.build_bundle(request=request)
        benchmarks = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))
                    
        fund = request.GET.get('funds', 0)
        funds = FundPerfMonthly.objects.filter(fund=fund, \
                    holding_group='all', holding_category__isnull=True)\
                    .latest('value_date')
     
        # rows
        rows = ['ann_return', 'ann_volatility', 'sharpe_ratio']
        data = []
        for index, row in enumerate(rows):
            dic = {}
            dic['type'] = row.title().replace('_', ' ')
            dic['fund_name'] = getattr(funds, row)
            for index, bench in enumerate(benchmarks):
                history = FundBenchHist.objects.filter(benchmark=bench.id).latest('value_date')
                dic['benchmark_' + str(index + 1)] = getattr(history, row)
            data.append(dic)
            
        # fund since inception
        funds = FundPerfYearly.objects.filter(fund=fund, \
                    holding_group='all', holding_category__isnull=True)\
                    .latest('year')
        print funds
        data.append({'type': 'Since Inception', 'fund_name': funds.si}) 
                    
        # columns
        fields = ['type', ['fund_name', funds.fund.name]]
        for index, field in enumerate(benchmarks):
            fields.append('benchmark_' + str(index + 1))  
        columns = self.set_columns(fields, [100, 100])

        dic = {
            'metaData': {'sorting': 'name'},
            'columns': columns,
            'rows': data,
        }
        return JsonResponse(dic)   
        
"""        
class FundBenchHistResource(MainBaseResource):
    user = fields.ForeignKey(FundBenchResource, 'benchmark', related_name='history')

    class Meta:
        queryset = FundBenchHist.objects.all()
        resource_name = 'history'
"""        
        
class FundBenchLineGraphResource(MainBaseResource):
    benchmark = fields.ForeignKey(FundBenchResource, 'benchmark', full=True)
        
    class Meta(MainBaseResource.Meta):
        queryset = FundBenchHist.objects.select_related('benchmark').all()
        filtering = {
            'benchmark': ALL_WITH_RELATIONS,
        }

    def get_list(self, request, **kwargs):



        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))

        # benchmarks
        # TODO: redo this
        dic = {}
        for row in objects:        
            date = int(mktime(row.value_date.timetuple())) * 1000
            output = [int(str(date)), row.value]
            bench_id = int(row.benchmark.id)
            
            try:
                dic[bench_id]['name'] = row.benchmark.name
            except:
                dic[bench_id] = {}
                dic[bench_id]['name'] = row.benchmark.name
            try:
                dic[bench_id]['data'].append(output)
            except:
                dic[bench_id]['data'] = []
                dic[bench_id]['data'].append(output)
                
        response_list = []
        for key, val in dic.iteritems():
            response_list.append(val)
        
        # funds    
        fund = request.GET.get('benchmark__funds', 0)
        funds = FundPerfMonthly.objects.select_related('fund') \
                        .filter(fund=fund, holding_group='all', \
                        holding_category__isnull=True)
                    
        dic = {}
        for row in funds:        
            date = int(mktime(row.value_date.timetuple())) * 1000
            output = [int(date), row.value]
            fund_id = int(row.fund.id)
            
            try:
                dic[fund_id]['name'] = row.fund.name
            except:
                dic[fund_id] = {}
                dic[fund_id]['name'] = row.fund.name
            try:
                dic[fund_id]['data'].append(output)
            except:
                dic[fund_id]['data'] = []
                dic[fund_id]['data'].append(output)
                
        for key, val in dic.iteritems():
            response_list.append(val)
        
        return JsonResponse(response_list)      

        
        
class HoldingCategoryResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = HoldingCategory.objects.all()



class HoldingTableResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    currency = fields.ForeignKey(CurrencyResource, 'currency', full=True)
    sector = fields.ForeignKey(HoldingCategoryResource, 'sector', full=True)
    sub_sector = fields.ForeignKey(HoldingCategoryResource, 'sub_sector', full=True)
    location = fields.ForeignKey(HoldingCategoryResource, 'location', full=True)
    #asset_class = fields.ForeignKey(HoldingCategoryResource, 'asset_class', full=True)


    class Meta(MainBaseResource.Meta):
        from django.db.models import Count
        queryset = Holding.objects.values('name').annotate(Count("id")).order_by().all() 
        queryset
        filtering = {
            "fund": ALL,
        }    
        fields = ['id', 'name', 'sector', 'sub_sector', 'location',\
               'currency', 'no_of_units', 'current_price', 'nav'] 
               
    def dehydrate(self, bundle):
        del bundle.data['fund']
        bundle.data['currency'] = bundle.data['currency'].data['name']
        bundle.data['sector'] = bundle.data['sector'].data['name']
        bundle.data['sub_sector'] = bundle.data['sub_sector'].data['name']
        bundle.data['location'] = bundle.data['location'].data['name']
        bundle.data['id'] = str(bundle.data['id'])
        #bundle.data['asset_class'] = bundle.data['asset_class'].data['name']
        
        return bundle
               
    def alter_list_data_to_serialize(self, request, data):
    
        fields = self._meta.fields
        for x in fields:
            if x == 'id':
                fields.remove(x)            
        columns = self.set_columns(fields, [80, 80])

        dic = {
            'metaData': {'sorting': 'name'},
            'columns': columns,
            'rows': data,
        }
        return dic



class FundPerfDataTableResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfYearly.objects.filter(holding_group='all')
        ordering = ['year', 'month']
        mandatory_params = ['fund']

        filtering = {
            "fund": ALL,
            "holding": ALL_WITH_RELATIONS,
        }
        
    def build_filters(self, filters=None):
        self.check_params(['fund'], filters)
        return super(MainBaseResource, self).build_filters(filters)

    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        years = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))

        fund = request.GET.get("fund", 0)
        fund = int(fund)

        # get the monthly values as well
        objects = FundPerfMonthly.objects.filter(fund__id=fund)

        # merge the 2 querysets into a list with dictionaries
        dic = {}
        newlist = []
        for year in years:
            dic = {
                'year': year.year,
                'si': year.si,
                'ytd': year.ytd
            }
            for row in objects:
                if row.year == year.year:
                    abbr = calendar.month_abbr[row.month]
                    dic[abbr.lower()] = row.value
            newlist.append(dic)
            
        # latest year first
        newlist.reverse()

        # create columns
        columns = ['year']
        for month in range(1, 13):
            abbr = calendar.month_abbr[month]
            columns.append(abbr.lower())
        append = ['si', 'ytd']
        [columns.append(add) for add in append]
        columns = self.set_columns(columns)

        dic = {
            'metaData': {
                #'root': 'rows',
                #"sortInfo": {
                #    "direction": "DESC",
                #    "field": "year"
                #},
            },
            'columns': columns,
            'rows': newlist,
        }
        return JsonResponse(dic)


# W3, W4 and W5 - Bar Graph
class HoldPerfMonthlyResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    holding_category = fields.ForeignKey(HoldingCategoryResource, 'holding_category', full=True, null=True)

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfMonthly.objects.select_related('holding_category').filter(holding_category__isnull=False)
        filtering = {
            "holding_group": ALL,
            "year": ALL,
            "fund": ALL,
        }

    def dehydrate(self, bundle):

        return bundle
        bundle.data = {
            'y': float(bundle.data['value']), #@TODO: Perm fix for float bug
            'name': bundle.data['holding'].data['name']
        }
        return bundle


    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))

        newlist = []
        categories = {}
        for obj in objects:
            try:
                categories[obj.holding_category.name][obj.month] = obj.value
            except:
                categories[obj.holding_category.name] = {}
                categories[obj.holding_category.name][obj.month] = obj.value

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

        dic = {
            'columns': columns,
            'objects': newlist,
        }
        return JsonResponse(dic)



# W2 Bar Graph
class HoldPerfBarGraphResource(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding', full=True,
                                null=True)

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfDaily.objects.select_related('holding') \
                                                .filter(holding__isnull=False)
        ordering = ['name', 'weight']
        include_resource_uri = False

        filtering = {
            "date": ALL,
            "fund": ALL,
        }

    """
    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))

        line_lis = []
        for hold in holding:
            date = int(mktime(hold.value_date.timetuple())) * 1000
            innerlis=[int(str(date)), hold.current_price]
            line_lis.append(innerlis)
              
        # trades for bar graph
        objects = Trade.objects.filter(identifier=identifier)
        bar_lis = []        
        for row in objects:            
            date = int(mktime(row.trade_date.timetuple())) * 1000
            innerlis=[int(str(date)), row.no_of_units]
            bar_lis.append(innerlis)
        return JsonResponse(dic)
    """
    
    def alter_list_data_to_serialize(self, request, data):
        dic = {}
        dic['columns'] = ''
        dic['objects'] = [{
            'data': data['objects'],
        }]
        return dic

    def dehydrate(self, bundle):
        data = {
            'y': float(bundle.data['value']), #@TODO: Perm fix for float bug
            'name': bundle.data['holding'].data['name']
        }
        return data
        
    # without date we would get thousands of records
    def build_filters(self, filters=None):
        self.check_params(['date'], filters)
        return super(MainBaseResource, self).build_filters(filters)


class FundPerfMonthTableResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfDaily.objects.filter(holding__isnull=True)
        ordering = ['name', 'weight']

        filtering = {
            "date": ALL,
            "fund": ALL,
        }


    def dehydrate(self, bundle):
        return {
            'date': bundle.data['date'],
            'value': bundle.data['value']
        }
        return bundle

    def build_filters(self, filters=None):
        return super(MainBaseResource, self).build_filters(filters)




class FundGroupPerfResource(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding', full=True)
    holding_category = fields.ForeignKey(HoldingCategoryResource, 'holding_category', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfYearly.objects.select_related('holding').all()
        ordering = ['name', 'weight']

        filtering = {
            "date": ALL,
            "fund": ALL,
            "year": ALL,
            #"holding": ALL_WITH_RELATIONS,
            "holding_group": ALL,
        }


    # without the fund we won't get any results
    # so we make it mandatory
    def build_filters(self, filters=None):
        self.check_params(['fund', 'holding_group'], filters)
        return super(FundGroupPerfResource, self).build_filters(filters)

    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        cats = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))

        holding_group = request.GET.get("holding_group", 0)
        fund = request.GET.get("fund", 0)
        fund = int(fund)

        # get the monthly values as well
        objects = FundPerfMonthly.objects.filter(
                            fund=fund, holding_group=holding_group)

        if holding_group == 'sec':
            group = 'sector'
        elif holding_group == 'sub':
            group = 'sub_sector'
        else:
            group = 'location'

        # merge the 2 querysets into a list with dictionaries
        dic = {}
        newlist = []
        for cat in cats:
            print cat.year
            dic = {
                group: cat.holding_category.name,
                'si': cat.si,
                'ytd': cat.ytd
            }
            for row in objects:
                if row.holding_category == cat.holding_category:
                    abbr = calendar.month_abbr[row.month]
                    dic[abbr.lower()] = row.value
            newlist.append(dic)

        # create columns
        columns = [group]
        for month in range(1, 13):
            abbr = calendar.month_abbr[month]
            columns.append(abbr.lower())
        append = ['si', 'ytd']
        [columns.append(add) for add in append]
        columns = self.set_columns(columns, (80, 50))

        dic = {
            'metaData': {'sorting': 'year', 'root': 'rows', },
            'columns': columns,
            'rows': newlist,
        }
        return JsonResponse(dic)


class FundPerfMonthlyResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfDaily.objects.all()

        filtering = {
            "year": ALL,
            "month": ALL
        }

    # fund param is mandatory
    def build_filters(self, filters=None):
        self.check_params(['fund'], filters)
        return super(FundPerfMonthlyResource, self).build_filters(filters)

    def get_object_list(self, request):
        objects = super(FundPerfMonthlyResource, self).get_object_list(request)

        try:
            # if we got both date params set we let tastypie do all the filtering
            request.GET['year']
            request.GET['month']
            return objects
        except:
            return objects.filter(
                year=datetime.date.today().year,
                month=datetime.date.today().month
            )


widget = Api(api_name="widget")
widget.register(InfoResource())
widget.register(UnusedResource())
widget.register(ConcernOccurrance())
widget.register(PieChart())
widget.register(Graph())
widget.register(ExampleTable1())
widget.register(FundGroupPerfResource())
widget.register(FundGroupPerfResource2())
widget.register(FundPerfDataTableResource())
widget.register(HoldingTableResource())
widget.register(HoldPerfBarGraphResource())
widget.register(FundPerfMonthTableResource())
widget.register(HoldPerfMonthlyResource())
widget.register(TradeTableResource())
widget.register(TradeBarGraphResource())
widget.register(FundBenchResource())
widget.register(FundBenchLineGraphResource())
widget.register(FundBenchDataTableResource())
