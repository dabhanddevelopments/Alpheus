from tastypie.resources import Resource, ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from tastypie import fields
from app.models import Page, PageWidget, Widget, WidgetType, Fund, FundType
from resources.base_resources import MainBaseResource
#from app import widget_models
from alpheus.serializers import PrettyJSONSerializer


from tastypie.api import Api


class WidgetBaseResource(MainBaseResource):

    """
    Base class for all widgets
    * Filters out all widgets the user does not have access to
    """
    class Meta(MainBaseResource.Meta):
        queryset = Widget.objects.all()

    def get_object_list(self, request):

        obj = super(WidgetBaseResource, self).get_object_list(request)

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

        # Description is only used for UnusedWidgetBaseResource
        del bundle.data['description']

        return bundle


class UnusedResource(InfoResource):

    """
    Returns unused widgets on the specified page
    """

    class Meta(InfoResource.Meta):

        filtering = {
            "page": ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data['widget_type'] = bundle.data['widget_type'].data['key']
        return bundle

    def get_object_list(self, request):

        obj = super(UnusedResource, self).get_object_list(request)

        # Filter out all the existing widgets on this Page
        existing_widgets = PageWidget.objects \
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
            { 'name': 'Bart',  "email":"bart@simpsons.com",  "phone":"555-222-1234" },
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

widget = Api(api_name="widget")
widget.register(InfoResource())
widget.register(UnusedResource())
widget.register(ConcernOccurrance())
widget.register(PieChart())
widget.register(Graph())
widget.register(ExampleTable1())


