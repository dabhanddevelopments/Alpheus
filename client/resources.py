from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields

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
