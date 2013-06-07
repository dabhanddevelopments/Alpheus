from tastypie.resources import Resource, ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from app.models import *
from resources.api import *
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
from datetime import date
#from datetime import timedelta
from alpheus.utils import JsonResponse
from alpheus import settings

# iniates the API
widget = Api(api_name="widget")

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



#####################################################################



# W1 Month View
# http://localhost:8008/api/widget/fundperfhistcalview/?fund=2&order_by=weight&value_date__year=2013&value_date__month=5&format=json
class FundPerfHistCalView(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta(MainBaseResource.Meta):
        queryset = FundPerf.objects.select_related('fund')
        ordering = ['value_date']

        filtering = {
            "value_date": ALL,
            "fund": ALL,
        }


    def dehydrate(self, bundle):
        return {
            'date': bundle.data['value_date'],
            'value': bundle.data['performance']
        }

    def build_filters(self, filters=None):
        return super(MainBaseResource, self).build_filters(filters)


widget.register(FundPerfHistCalView())





# W1, W18 Data Table
# http://localhost:8000/api/widget/fundperfmonth/?format=json&fund=2&fields=performance
class FundPerfMonth(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfMonth.objects.select_related('fund')
        ordering = ['value_date']

        filtering = {
            "value_date": ALL,
            "fund": ALL,
        }

    def build_filters(self, filters=None):
        self.check_params(['fields'], filters)
        return super(MainBaseResource, self).build_filters(filters)

    def alter_list_data_to_serialize(self, request, data):

        fields = request.GET.get("fields", 0)
        lis = []
        dic = {}
        this_year = date.today().year

        for row in data['objects']:

            for year in range(1970, this_year + 1):

                value_date = row.data['value_date']

                if year == value_date.year:
                    try:
                        dic[year]
                    except:
                        dic[year] = {'year': year}

                    for month in range(1, 13):

                        if month == value_date.month:

                            name = calendar.month_abbr[value_date.month]
                            dic[year][name.lower()] = row.data[fields]

                            if month == 12:
                                dic[year]['ytd'] = row.data['ytd']

        for key, val in dic.iteritems():
            lis.append(val)

        # create columns
        columns = ['year']
        for month in range(1, 13):
            abbr = calendar.month_abbr[month]
            columns.append(abbr.lower())
        if fields == 'performance':
            columns.append('ytd')
        columns = self.set_columns(columns, [50, 50])

        dic = {
            'sorting': 'year',
            'columns': columns,
            'rows': lis,
        }

        return dic
widget.register(FundPerfMonth())



# W2, W8 Graph
# http://localhost:8007/api/widget/fundperfholdperfbar/?fund=2&value_date=2013-5-30&legend=false&format=json
class FundPerfHoldPerfBar(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    holding = fields.ForeignKey(HoldingResource, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerfMonth.objects.select_related('fund', 'holding')
        ordering = ['name', 'weight']
        #fields = ['current_price', 'holding__name']

        filtering = {
            "value_date": ALL,
            "fund": ALL,
        }

    def alter_list_data_to_serialize(self, request, data):
        dic = {}
        dic['objects'] = [{
            'data': data['objects'],
        }]
        return dic

    def dehydrate(self, bundle):
        fields = bundle.request.GET.get('fields', 0)
        data = {
            'y': float(bundle.data[fields]), #@TODO: Perm fix for float bug
            'name': bundle.data['holding'].data['name']
        }
        return data

    # without date we would get thousands of records
    def build_filters(self, filters=None):
        self.check_params(['fields'], filters)
        return super(MainBaseResource, self).build_filters(filters)
widget.register(FundPerfHoldPerfBar())


# FORMER W2. WILL BE USED IN THE FUTURE FOR OTHER WIDGETS
class FundPerfHoldPerf(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerf.objects.select_related('holding', 'holding__fund')
        ordering = ['name', 'weight']
        #fields = ['current_price', 'holding__name']

        filtering = {
            "value_date": ALL,
            "holding": ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):
        dic = {}
        dic['objects'] = [{
            'data': data['objects'],
        }]
        return dic

    def dehydrate(self, bundle):
        data = {
            'y': float(bundle.data['performance']), #@TODO: Perm fix for float bug
            'name': bundle.data['holding'].data['name']
        }
        return data

    # without date we would get thousands of records
    def build_filters(self, filters=None):
        self.check_params(['value_date'], filters)
        return super(MainBaseResource, self).build_filters(filters)
widget.register(FundPerfHoldPerf())




# W3, W4, W5, W8, W9, W10 Data Table
# http://localhost:8007/api/widget/fundperfgrouptable/?fund=2&value_date__year=2013&holding_category__holding_group=loc&format=json&fields=performance
class FundPerfGroupTable(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    holding_category = fields.ForeignKey(HoldingCategoryResource, 'holding_category', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerfMonth.objects.select_related('holding_category', 'fund')
        ordering = ['name', 'weight']

        filtering = {
            "value_date": ALL,
            "fund": ALL,
            'holding_category': ALL_WITH_RELATIONS,
        }


    # without the fund we won't get any results
    # so we make it mandatory
    def build_filters(self, filters=None):
        self.check_params(['fund', 'holding_category__holding_group', 'fields', 'value_date__year'], filters)
        return super(FundPerfGroupTable, self).build_filters(filters)


    def alter_list_data_to_serialize(self, request, data):

        fields = request.GET.get("fields", 0)
        holding_group = request.GET.get("holding_category__holding_group", 0)

        lis = []
        dic = {}
        this_year = date.today().year

        if holding_group == 'sec':
            group = 'sector'
        elif holding_group == 'sub':
            group = 'sub_sector'
        else:
            group = 'location'

        for row in data['objects']:

            value_date = row.data['value_date']
            cat_id = row.data['holding_category'].data['id']
            try:
                dic[cat_id]
            except:
                dic[cat_id] = {
                    group: row.data['holding_category'].data['name']
                }
            for month in range(1, 13):

                if month == value_date.month:

                    name = calendar.month_abbr[value_date.month]
                    dic[cat_id][name.lower()] = row.data[fields]

                    if month == 12:
                        dic[cat_id]['ytd'] = row.data['ytd']
                        dic[cat_id]['si'] = row.data['ytd']

        for key, val in dic.iteritems():
            lis.append(val)


        # create columns
        columns = [group]
        for month in range(1, 13):
            abbr = calendar.month_abbr[month]
            columns.append(abbr.lower())

        # not NAV
        if fields == 'performance':
            columns.append('si')
            columns.append('ytd')

        columns = self.set_columns(columns, (80, 50))

        dic = {
            'metaData': {'sorting': 'year', 'root': 'rows', },
            'columns': columns,
            'rows': lis,
        }
        return dic
widget.register(FundPerfGroupTable())



# W3, W4 and W5 - Bar Graph
# http://localhost:8009/api/widget/fundperfgroupbar/?year__fund=2&value_date__year=2013&holding_category__holding_group=loc&format=json
class FundPerfGroupBar(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    holding_category = fields.ForeignKey(HoldingCategoryResource, 'holding_category')

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerfMonth.objects.select_related('holding', 'holding_category')
        filtering = {
            "fund": ALL,
            "holding_category": ALL_WITH_RELATIONS,
            "value_date": ALL,
        }

    def dehydrate(self, bundle):

        return bundle # ????
        bundle.data = {
            'y': float(bundle.data['performance']), #@TODO: Perm fix for float bug
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
                categories[obj.holding_category.name][obj.value_date.month] = obj.performance
            except:
                categories[obj.holding_category.name] = {}
                categories[obj.holding_category.name][obj.value_date.month] = obj.performance

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
widget.register(FundPerfGroupBar())



# W7 Bar Graph
# http://localhost:8007/api/widget/fundallocnavbar/?holding__fund=2&value_date=2013-5-30&legend=false&format=json
# @TODO: join this resource with W2
class FundAllocNavBar(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerf.objects.select_related('holding', 'holding__fund')
        ordering = ['name', 'weight']
        #fields = ['current_price', 'holding__name']

        filtering = {
            "value_date": ALL,
            "holding": ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):
        dic = {}
        dic['objects'] = [{
            'data': data['objects'],
        }]
        return dic

    def dehydrate(self, bundle):
        data = {
            'y': float(bundle.data['nav']), #@TODO: Perm fix for float bug
            'name': bundle.data['holding'].data['name']
        }
        return data

    # without date we would get thousands of records
    def build_filters(self, filters=None):
        self.check_params(['value_date'], filters)
        return super(MainBaseResource, self).build_filters(filters)


widget.register(FundAllocNavBar())



# W8, W9, W10 Pie Chart
# http://localhost:8009/api/widget/fundnavpie/?year__fund=2&value_date=2013-12-01&holding_category__holding_group=sec&legend=false&format=json
class FundNavPie(MainBaseResource):
    year = fields.ForeignKey(HoldingResource, 'year')
    holding_category = fields.ForeignKey(HoldingCategoryResource, 'holding_category', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerfMonth.objects.select_related('year', 'holding_category')
        filtering = {
            "year": ALL_WITH_RELATIONS,
            "value_date": ALL,
            "holding_category": ALL_WITH_RELATIONS,
        }


    def alter_list_data_to_serialize(self, request, data):
        dic = {}
        dic['objects'] = [{
            'data': data['objects'],
        }]
        return dic

    def dehydrate(self, bundle):
        data = {
            'y': float(bundle.data['nav']), #@TODO: Perm fix for float bug
            'name': bundle.data['holding_category'].data['name']
        }
        return data

    # without date we would get thousands of records
    def build_filters(self, filters=None):
        self.check_params(['value_date'], filters)
        return super(MainBaseResource, self).build_filters(filters)


widget.register(FundNavPie())






# W11 holding table
# http://localhost:8000/api/widget/fundperfholdtable/?format=json&fund=2
class FundPerfHoldTable(MainBaseResource):


    fund = fields.ForeignKey(FundResource, 'fund')
    currency = fields.ForeignKey(CurrencyResource, 'currency', full=True)
    sector = fields.ForeignKey(HoldingCategoryResource, 'sector', \
                                     related_name='sec', full=True)
    sub_sector = fields.ForeignKey(HoldingCategoryResource, 'sub_sector', \
                                        related_name='sub_sec', full=True)
    location = fields.ForeignKey(HoldingCategoryResource, 'location', \
                                    related_name='loc', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Holding.objects.select_related('currency', 'sector', \
                                    'fund', 'sub_sector', 'location').all()
        filtering = {
            'fund': ALL,
        }
        fields = [
            'id',
            'name',  'no_of_units',
            'current_price', 'nav',
            'sector__name',
            'sub_sector__name',
            'location__name',
            'currency__name',
        ]

    def alter_list_data_to_serialize(self, request, data):

        fields = self._meta.fields;
        if 'id' in fields: fields.remove('id')

        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(fields, [80, 80]),
            'rows': data,
        }
        return data

widget.register(FundPerfHoldTable())



# W11 - Trade Volume Bar Graph
# http://localhost:8007/api/widget/fundperfholdvolbar/?format=json&holding__fund=2
class FundPerfHoldVolBar(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding')
    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.select_related('holding').all()
        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):
        lis = []
        for row in data['objects']:
            date = int(mktime(row.data['trade_date'].timetuple())) * 1000
            innerlis=[int(str(date)), float(row.data['no_of_units'])]
            lis.append(innerlis)
        return lis
widget.register(FundPerfHoldVolBar())


# W11 - Holding Price Line Graph
# http://localhost:8007/api/widget/fundperfholdpriceline/?format=json&holding__fund=2
class FundPerfHoldPriceLine(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding')

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerf.objects.select_related('holding').all()
        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):
        lis = []
        for row in data['objects']:
            date = int(mktime(row.data['value_date'].timetuple())) * 1000
            innerlis=[int(str(date)), float(row.data['current_price'])]
            lis.append(innerlis)
        return lis
widget.register(FundPerfHoldPriceLine())


# W11 - Holding Trade Inner Table
# http://localhost:8007/api/widget/fundperfholdtradetable/?format=json&holding__fund=2
class FundPerfHoldTradeTable(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding')
    purchase_sale = fields.ForeignKey(PurchaseSaleResource, 'purchase_sale', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.select_related('holding', 'purchase_sale').all()
        fields = ['trade_date', 'settlement_date', 'purchase_sale__name',
            'no_of_units', 'purchase_price_base', 'fx_to_euro',
            'purchase_price', 'nav_purchase',]
        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):
        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(self._meta.fields, [80, 80]),
            'rows': data,
        }
        return data
widget.register(FundPerfHoldTradeTable())



# W16 Line Graph NOT USED ATM - views.py
# @TODO: optimize query
# http://localhost:8007/api/widget/fundperfbenchcompline/?format=json&benchmark__funds=2
class FundPerfBenchCompLine(MainBaseResource):

    benchmark = fields.ForeignKey(FundBenchResource, 'benchmark', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = FundBenchHist.objects.select_related('benchmark')
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
            output = [int(str(date)), row.performance]
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
        fields = request.GET.get("fields", 0)
        fund = request.GET.get('benchmark__funds', 0)
        funds = FundPerfMonth.objects.select_related('fund') \
                                                .filter(fund=fund)

        dic = {}
        for row in funds:
            date = int(mktime(row.value_date.timetuple())) * 1000
            output = [int(date), row.performance] #getattr(row, fields)]
            fund_id = int(row.year.fund.id)

            try:
                dic[fund_id]['name'] = row.year.fund.name
            except:
                dic[fund_id] = {}
                dic[fund_id]['name'] = row.year.fund.name
            try:
                dic[fund_id]['data'].append(output)
            except:
                dic[fund_id]['data'] = []
                dic[fund_id]['data'].append(output)

        for key, val in dic.iteritems():
            response_list.append(val)

        return JsonResponse(response_list)


widget.register(FundPerfBenchCompLine())


# W16 Data Table NOT USED ATM - views.py
# @TODO: Rewrite this. Maybe use a reverse relation instead
# http://localhost:8000/api/widget/befundperfbenchcomptable/?funds=2&format=json
class FundPerfBenchCompTable(MainBaseResource):

    funds = fields.ToManyField(FundResource, 'funds', related_name='asdf')

    class Meta(MainBaseResource.Meta):
        queryset = FundBench.objects.all()
        filtering = {
            "funds": ALL,
        }

    # fund param is mandatory
    def build_filters(self, filters=None):
        self.check_params(['funds'], filters)
        return super(FundPerfBenchCompTable, self).build_filters(filters)

    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        benchmarks = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))

        FundPerfMonth.objects.select_related('fund')
        fund = request.GET.get('funds', 0)
        funds = FundPerfMonth.objects.select_related('fund') \
                            .filter(year__fund=fund).latest('value_date')

        # rows
        rows = ['ann_return1', 'ann_volatility1', 'sharpe_ratio1']
        data = []
        for index, row in enumerate(rows):
            dic = {}
            dic['type'] = row.title().replace('_', ' ')
            dic['fund_name'] = getattr(funds, row)
            for index, bench in enumerate(benchmarks):
                history = FundBenchHist.objects.filter(benchmark=bench.id) \
                                                        .latest('value_date')
                dic['benchmark_' + str(index + 1)] = getattr(history, row)
            data.append(dic)

        # get latest SI
        funds = FundPerfMonth.objects.filter(fund=fund).latest('value_date')
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
widget.register(FundPerfBenchCompTable())







"""
class HoldPerfResource(MainBaseResource):
    holding = fields.ForeignKey(HoldingResourceDetail, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = HoldPerf.objects.select_related(
            'holding', 'holding__currency', 'holding__sector',
            'holding__sub_sector', 'holding__location', 'holding__fund',
        ).all()

        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }
"""










"""
class FundBenchHistResource(MainBaseResource):
    user = fields.ForeignKey(FundBenchResource, 'benchmark', related_name='history')

    class Meta:
        queryset = FundBenchHist.objects.all()
        resource_name = 'history'
"""












class HoldTradeResource(ModelResource):
    holding = fields.ForeignKey(HoldingResource, 'holding', full=True)
    class Meta:
        queryset = HoldPerf.objects.select_related('holding').all()#.latest('value_date')
        #fields = ['nav', 'holding__name']

    # fetch only the latest if the id isn't supplied
    def obj_get_list(self, request=None, **kwargs):
        asdf = HoldPerf.objects.select_related('holding').all().latest('value_date')

        return super(HoldTradeResource, self).get_object_list(request).all().latest('value_date')
    #    print asdf
    #    return asdf

    #def get_object_list(self, request):
    #    print request.GET
    #    return super(HoldTradeResource, self).get_object_list(request).all()

    #def dispatch(self, request_type, request, **kwargs):
    #    print request_type



    def dehydrate(self, bundle):

        #fields = ['
        #print bundle.data['holding']
        return bundle



class HoldLiquidity(MainBaseResource):
    holding = fields.ForeignKey(HoldingResourceFund, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.select_related('holding', 'holding__fund').all()
        fields = [
            'holding__nav', 'holding__redemption_frequency',
            'holding__redemption_notice', 'holding__max_redemption',
            'holding__payment_days', 'dealing_date',
            'holding__gate', 'holding__soft_lock',
            'holding__redemption_fee12', 'holding__redemption_fee24',
            'holding__redemption_fee36', 'holding__name',
        ]
        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):

        # columns we want to rename
        # @TODO: move this to set_columns()
        columns = [
            'holding',
            'nav',
            ['redemption_frequency', 'Red\'n Freq.'],
            ['redemption_notice', 'Red\'n Notice'],
            ['max_redemption', 'Max Red\'n'],
            'holding__payment_days',
            'dealing_date',
            'gate',
            'soft_lock',
            ['redemption_fee12', 'Red\'n Fee 12M'],
            ['redemption_fee24', 'Red\'n Fee 24M'],
            ['redemption_fee36', 'Red\'n_Fee_36M'],
        ]
        """
        columns = []
        for field in self._meta.fields:
            field = field.replace('holding__', '')
            if field != 'name':
                try:
                    columns.append([field, special_columns[field]])
                except:
                    columns.append(field)
        columns = ['holding'] + columns
        """
        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(columns, [100, 85]),
            'rows': data['objects'],
        }
        return data
widget.register(HoldLiquidity())



class RedemptionTracker(MainBaseResource):
    holding = fields.ForeignKey(HoldingResourceFund, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.select_related('holding', 'holding__fund').all()
        fields = [
            'nav_purchase', 'holding__weight',
            'dealing_date', 'holding__name',
        ]
        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):
        columns = ['holding', 'amount', 'weight', ['redemption_date', 'Red\'n Date']]
        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(columns, [100, 85]),
            'rows': data['objects'],
        }
        return data
widget.register(RedemptionTracker())



class RedemptionTracker(MainBaseResource):
    holding = fields.ForeignKey(HoldingResourceFund, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.select_related('holding', 'holding__fund').all()
        fields = [
            'nav_purchase', 'holding__cumulative_weight',
            'holding__cumulative_nav', 'dealing_date', 'holding__name',
        ]
        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }

    def alter_list_data_to_serialize(self, request, data):
        columns = ['holding', 'amount', 'weight', ['redemption_date', 'Red\'n Date']]
        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(columns, [100, 85]),
            'rows': data['objects'],
        }
        return data
widget.register(RedemptionTracker())




class CumulativeWeight(MainBaseResource):
    holding = fields.ForeignKey(HoldingResourceFund, 'holding', full=True)

    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.select_related('holding', 'holding__fund').all()
        fields = [
            'nav_purchase', 'holding__cumulative_weight',
            'holding__cumulative_nav', 'dealing_date', 'holding__weight',
        ]
        filtering = {
            'holding': ALL_WITH_RELATIONS,
        }

class CumulativeWeightTable(CumulativeWeight):
    holding = fields.ForeignKey(HoldingResourceFund, 'holding', full=True)
    class Meta(CumulativeWeight.Meta):
        pass

    def dehydrate(self, bundle):
        bundle = super(CumulativeWeightTable, self).dehydrate(bundle)
        del bundle.data['holding']
        return bundle

    def alter_list_data_to_serialize(self, request, data):

        columns = [['dealing_date', 'Red\'n Date'], 'cumulative_nav', 'weight',
                   ['cumulative_weight', 'Cum. Weight']]
        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(columns, [100, 85]),
            'rows': data['objects'],
        }
        return data
widget.register(CumulativeWeightTable())

class CumulativeWeightGraph(CumulativeWeight):
    holding = fields.ForeignKey(HoldingResourceFund, 'holding', full=True)
    class Meta(CumulativeWeight.Meta):
        pass

    def dehydrate(self, bundle):
        bundle = super(CumulativeWeightGraph, self).dehydrate(bundle)
        del bundle.data['holding']
        return bundle

    def alter_list_data_to_serialize(self, request, data):

        y1 = []
        y2 = []
        x = []
        for row in data['objects']:
            date = int(mktime(row.data['dealing_date'].timetuple())) * 1000
            y1.append([date, float(row.data['cumulative_weight'])])
            y2.append([date, float(row.data['cumulative_nav'])])
        data = [{
            'data': y1,
            'yAxis': 0,
        },{
            'data': y2,
            'yAxis': 1,
            #'type': 'line',
        #},{
        #    'data': x,
        #    'xAxis': 1,
        }]
        return data
widget.register(CumulativeWeightGraph())

class FundSummary(MainBaseResource):
    fund_type = fields.ForeignKey(FundTypeResource,'fund_type', full=True)
    benchmark = fields.ForeignKey(FundBenchResource, 'benchmark', null=True, full=True)
    custodian = fields.ForeignKey(CustodianResource, 'custodian', full=True)
    auditor = fields.ForeignKey(AuditorResource, 'auditor', full=True)
    administrator =  fields.ForeignKey(AdministratorResource, 'administrator', full=True)
    classification = fields.ForeignKey(ClassificationResource, 'classification', full=True)
    manager = fields.ForeignKey(UserResource, 'manager', full=True)
    
    
    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.select_related('fund_type', 'benchmark',\
         'custodian', 'auditor', 'administrator', 'classification', \
         'manager')

widget.register(FundSummary())


# @TODO limit columns
class FundRegister(MainBaseResource):
    fund = fields.ManyToManyField(FundResource, 'fund')
    
    class Meta(MainBaseResource.Meta):
        queryset = Client.objects.prefetch_related('fund')
        filtering = {
            'fund': ALL,
        }
    def dehydrate(self, bundle):
        bundle.data['name'] = bundle.data['first_name'] + ' ' + bundle.data['last_name']
        return bundle
        
    def alter_list_data_to_serialize(self, request, data):

        columns = [['name', 'Client'], ['no_of_units', 'No of Units'],
                   ['nav', 'NAV'], ['pending_nav', 'Pending NAV']]
        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(columns, [115, 130]),
            'rows': data['objects'],
        }
        return data
widget.register(FundRegister())

"""
not used - moved to views becaue of get_FOO_display()
class SubscriptionRedemption(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    client = fields.ForeignKey(ClientResource, 'client')
    
    class Meta(MainBaseResource.Meta):
        queryset = SubscriptionRedemption.objects.all()
        filtering = {
            'fund': ALL,
            'client': ALL,
        }
    def dehydrate(self, bundle):
        bundle.data['sub_red'] = bundle.get_sub_red_display()
        bundle.data['percent_released'] = bundle.data['percent_released'].get_percent_released_display()
        
    def alter_list_data_to_serialize(self, request, data):

        columns = [['name', 'Sub. or Red.'], 'trade_date',
                   ['no_of_units', 'No. of Units'], ['pending_nav', 'NAV of Trance'],
                   'percent_released']
        data = {
            'metaData': {'sorting': 'name'},
            'columns': self.set_columns(columns, [100, 85]),
            'rows': data['objects'],
        }
        return data
widget.register(SubscriptionRedemption())
"""

"""
# not used?
class FundPerfMonthResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = FundPerf.objects.all()

        filtering = {
            "value_date": ALL
        }

    # fund param is mandatory
    def build_filters(self, filters=None):
        self.check_params(['fund'], filters)
        return super(FundPerfMonthResource, self).build_filters(filters)

    def get_object_list(self, request):
        objects = super(FundPerfMonthResource, self).get_object_list(request)

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
"""


widget.register(InfoResource())
widget.register(UnusedResource())
