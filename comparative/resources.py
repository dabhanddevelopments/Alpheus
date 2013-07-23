from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields

from comparative.models import * 
from alpheus.base_resources import MainBaseResource

class BenchmarkResource(MainBaseResource):
    fund = fields.ManyToManyField('fund.FundResource', 'fund')
    
    class Meta:
        queryset = Benchmark.objects.all()
        resource_name = 'benchmark'
        filtering = {
            "fund": ALL,
            "value_date": ALL,
        }
        
class BenchmarkHistoryResource(MainBaseResource):
    
    class Meta:
        queryset = BenchmarkHistory.objects.all()
        resource_name = 'benchmark-history'
        filtering = {
            "value_date": ALL,
            'date_type': ALL,
        }
        

class PeerResource(MainBaseResource):
    holding = fields.ForeignKey('holding.HoldingResource', 'holding')

    class Meta(MainBaseResource.Meta):
        queryset = Peer.objects.all() 
        resource_name = 'peer'
        filtering = {
            "holding": ALL,
            "value_date": ALL,
            "date_type": ALL,
        }


class PeerHistoryResource(MainBaseResource):
    peer = fields.ForeignKey(PeerResource, 'peer')
    holding = fields.ForeignKey('holding.HoldingResource', 'holding')

    class Meta(MainBaseResource.Meta):
        queryset = PeerHistory.objects.all() 
        resource_name = 'peer-history'
        filtering = {
            "holding": ALL,
            "peer": ALL,
            "value_date": ALL,
            "date_type": ALL,
        }

