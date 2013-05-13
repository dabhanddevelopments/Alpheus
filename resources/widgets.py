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



class FundYearPerfResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta(MainBaseResource.Meta):
        queryset = FundPerfYearly.objects.filter(holding_group='all')
        ordering = ['year', 'month']
        mandatory_params = ['fund']

        filtering = {
            "fund": ALL,
            "holding": ALL_WITH_RELATIONS,
        }

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

        # create columns
        columns = ['year']
        for month in range(1, 13):
            abbr = calendar.month_abbr[month]
            columns.append(abbr.lower())
        append = ['si', 'ytd']
        [columns.append(add) for add in append]
        columns = self.month_columns(columns)

        dic = {
            'metaData': {'sorting': 'year', 'root': 'rows', },
            'columns': columns,
            'rows': newlist,
        }
        return JsonResponse(dic)




class HoldPerfResource(MainBaseResource):
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

    def dehydrate(self, bundle):

        bundle.data = {
            'y': float(bundle.data['value']), #@TODO: Perm fix for float bug
            'name': bundle.data['holding'].data['name']
        }
        return bundle

    # without date we would get thousands of records
    def build_filters(self, filters=None):
        self.check_params(['date'], filters)
        return super(MainBaseResource, self).build_filters(filters)


class FundPerfResource(MainBaseResource):

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



class HoldingCategoryResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = HoldingCategory.objects.all()

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
            "holding": ALL_WITH_RELATIONS,
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
        print holding_group
        print objects

        if holding_group == 'sec':
            group = 'sector'
        elif holding_group == 'sub':
            group = 'sub_sector'
        else:
            group == 'loc'

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
        columns = self.month_columns(columns)

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
widget.register(FundYearPerfResource())
widget.register(HoldPerfResource())
widget.register(FundPerfResource())

