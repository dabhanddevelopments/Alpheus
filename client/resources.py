from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.resources import Resource, ModelResource

from client.models import *
from alpheus.base_resources import MainBaseResource
from fund.resources import FundResource

class ClientResource(MainBaseResource):
    fund = fields.ManyToManyField(FundResource, 'fund', related_name='fund')

    class Meta(MainBaseResource.Meta):
        queryset = Client.objects.all()
        ordering = ['last_name']
        filtering = {
            'fund': ALL_WITH_RELATIONS,
        }

class ClientHistoryResource(MainBaseResource):
    client = fields.ForeignKey(ClientResource, 'client')
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta(MainBaseResource.Meta):
        queryset = ClientHistory.objects.all()
        resource_name = 'client-history'
        ordering = ['last_name', 'performance']
        filtering = {
            'client': ALL_WITH_RELATIONS,
            'fund': ALL_WITH_RELATIONS,
            'date_type': ALL,
            'value_date': ALL,
        }

class SubscriptionRedemptionResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    client = fields.ForeignKey(ClientResource, 'client')

    class Meta(MainBaseResource.Meta):
        queryset = SubscriptionRedemption.objects.all()
        resource_name = 'subscription-redemption'
        filtering = {
            'fund': ALL,
            'client': ALL,
        }



