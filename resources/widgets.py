from tastypie.resources import Resource, ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from app.models import *
from resources.api import FundResource
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



class MetaPaginator(Paginator):
    def page(self):
        output = super(MetaPaginator, self).page()

        #print 'asdf'
        #print output
        # First keep a reference.
        return output

class FundPerfYearlyResource(MainBaseResource):

    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta(MainBaseResource.Meta):
        queryset = FundPerformanceYearly.objects.all()
        ordering = ['year', 'month']
        paginator_class = MetaPaginator
        mandatory_params = ['fund']

        filtering = {
            "fund": ALL,
        }

    # fund param is mandatory
    def build_filters(self, filters=None):
        self.check_params(['fund'], filters)
        return super(FundPerfYearlyResource, self).build_filters(filters)

    def get_list(self, request, **kwargs):

        """
        from django.utils.datastructures import SortedDict
        select=SortedDict([
            ('yi', "SELECT AVG(value) FROM app_historicalholding WHERE date > %s and date < %s"),
            ('si', "SELECT AVG(value) FROM app_historicalholding WHERE date > %s and date < %s"),
            ('year', "EXTRACT(year FROM date)"),
            ('month', "EXTRACT(month FROM date)"),
        ])
        year = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs)).extra(select, \
                                    select_params=("2012-01-01", "2013-01-01")) \
                    .values('year', 'month', 'yi').annotate(Avg('value'))

        select = {
            'year': "EXTRACT(year FROM date)",
            'month': "EXTRACT(month FROM date)",
        }
        """

        base_bundle = self.build_bundle(request=request)
        years = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs))


        fund = request.GET.get("fund", 0)
        fund = int(fund)

        # get the monthly values as well
        objects = FundPerformanceMonthly.objects.filter(fund__id=fund)


        dic = {}
        newlist = []
        for year in years:
            dic = {
                'si': year.si,
                'ytd': year.ytd
            }
            for row in objects:
                print row
                if row.year == year.year:
                    abbr = calendar.month_abbr[row.month]
                    dic[abbr.lower()] = row.value
            newlist.append(dic)

        columns = []
        for month in range(1, 13):
            abbr = calendar.month_abbr[month]
            columns.append(abbr.lower())

        append = ['si', 'year', 'ytd']
        [columns.append(add) for add in append]

        columns = self.month_columns(columns)

        dic = {
            'metaData': {'sorting': 'year', 'root': 'rows', },#'fields': fields},
            'columns': columns,
            'rows': newlist,
        }
        return JsonResponse(dic)

class FundPerfMonthlyResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = FundPerformanceMonthly.objects.all()

        filtering = {
            "date": ALL,
        }

    # fund param is mandatory
    def build_filters(self, filters=None):
        self.check_params(['fund'], filters)
        return super(FundPerfMonthlyResource, self).build_filters(filters)

    def get_object_list(self, request):
        return super(MyResource,
            self).get_object_list(request).filter(
                date__year=int(request.GET.get('year',
                                               datetime.date.today().year())),
                date__month=int(request.GET.get('month', datetime.date.today().year()))
                start_date__gte=now
            )
    def get_list2(self, request, **kwargs):

        """
        Create dictionary of days in month
        Weekends are empty
        """

        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
        except:
            year = datetime.date.today().year
            month = datetime.date.today().month

        date = datetime.date(year, month, 1)
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]

        select={'day': "EXTRACT(day FROM date)"}

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs)).extra(select) \
                    .filter(date__year=year, date__month=month)

        print objects

        dic = {}
        d = date
        end = datetime.date(date.year, date.month, last_day_of_month)
        delta = datetime.timedelta(days=1)
        weekend = set([5, 6])
        while d <= end:
            for row in objects:
                if d.day == row['day']:
                    dic[d.day] = row['value__avg']
            try:
                dic[d.day]
            except:
                if d.weekday() not in weekend:
                    dic[d.day] = 0
                else:
                    dic[d.day] = '' # weekend
            d += delta

        return JsonResponse(dic)
        return HttpResponse(json.dumps(dic))

class FundPerfHoldResource(ModelResource):

    """
    Get average historical performance for a given day
    """

    class Meta:
        queryset = FundPerformanceMonthly.objects.all()

        filtering = {
            "date": ALL,
        }

    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)
        obj = self.obj_get_list(bundle=base_bundle,
                    **self.remove_api_resource_names(kwargs)) \
                    .values('holding__name').annotate(Avg('value')).order_by()

        lis = []
        for row in obj:
            dic = {}
            dic['name'] = row['holding__name']
            dic['data'] = [row['value__avg']]
            lis.append(dic)
        return JsonResponse(lis)


widget = Api(api_name="widget")
widget.register(InfoResource())
widget.register(UnusedResource())
widget.register(ConcernOccurrance())
widget.register(PieChart())
widget.register(Graph())
widget.register(ExampleTable1())
widget.register(FundPerfYearlyResource())
widget.register(FundPerfMonthlyResource())
widget.register(FundPerfHoldResource())

