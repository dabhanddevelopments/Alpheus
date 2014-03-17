from tastypie import fields
from alpheus.base_resources import MainBaseResource
from tastypie.resources import Resource, ModelResource
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from v2.models import *
from alpheus.utils import cumulative_return
from datetime import datetime, timedelta
import decimal
import numpy as np
import pandas as pd
from django.utils.datastructures import SortedDict

class AdministratorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Administrator.objects.all()

class AlarmResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Alarm.objects.all()

class GroupResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = AlpheusGroup.objects.all()

class AssetClassResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = AssetClass.objects.all()

class AuditorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Auditor.objects.all()

class BenchComponentResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = BenchComponent.objects.all()

class BenchPeerResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = BenchPeer.objects.all()

class BrokerResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Broker.objects.all()

class CounterPartyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = CounterParty.objects.all()

class CountryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Country.objects.all()

class CurrencyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Currency.objects.all()

class CurrencyRateResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = CurrencyRate.objects.all()

class CustodianResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Custodian.objects.all()

class FeeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Fee.objects.all()

class FundStyleResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundStyle.objects.all()

class GicsCategoryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = GicsCategory.objects.all()

class HfSectorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HfSector.objects.all()

class IcbCategoryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IcbCategory.objects.all()

class IndustryGroupResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IndustryGroup.objects.all()

class IndustrySectorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IndustrySector.objects.all()

class IndustrySubGroupResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IndustrySubGroup.objects.all()

class IssuerIndustryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IssuerIndustry.objects.all()

class ManagerResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Manager.objects.all()

class RegionResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Region.objects.all()

class ClientPositionAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = ClientPositionAudit.objects.all()

class ClientResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Client.objects.all()

class ClientTransactionsResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = ClientTransaction.objects.all()

class ClientValAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = ClientValAudit.objects.all()

class FundFeeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundFee.objects.all()

class FundFeeAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundFeeAudit.objects.all()

class FundPeerResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundPeer.objects.all()

class FundPositionAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundPositionAudit.objects.all()

class FundResource(MainBaseResource):
    benchpeer = fields.ForeignKey(BenchPeer, "benchpeer")
    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()

class FundCharAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundCharAudit.objects.all()


class FundReturnResource(MainBaseResource):

    def alter_list_data_to_serialize(self, request, data):            
    
        # Histogram
        if request.GET.get('histogram', False):
        
            lst = [row.data['fund_perf'] for row in data['objects']]
            
            hist = np.histogram(lst, bins=21, range=(-10,11), density=False)
            
            values = [int(row) for row in hist[0]]
            keys = [row for row in hist[1]]
                
            data = {
                'data': values,
                'columns': keys,
            }
            
            return data
            
        # cumulative return
        y1 = request.GET.get('y1', False)

        if y1 != False:
            
            # create new previous dummy month
            first_date = data['objects'][0].data['value_date']
            new_date = datetime(first_date.year, first_date.month, 1) - timedelta(days=1)
            new_date = datetime(new_date.year, new_date.month, 1)
            
            new_data = {
                'fund_perf': decimal.Decimal('0'), 
                'value_date': new_date, 
                'bench_perf': decimal.Decimal('0')
            }
            new_obj = self.build_bundle(data = new_data)
            data['objects'].insert(0, new_obj)
            
            data = cumulative_return(data, perf_type = 'fund')
            data = cumulative_return(data, perf_type = 'bench')
            
            
            # delta
            if request.GET.get("graph_type", False) == 'bench':
                for id, row in enumerate(data['objects']):
                    data['objects'][id].data['fund_perf'] = row.data['fund_perf'] - row.data['bench_perf']

        return super(FundReturnResource, self) \
                .alter_list_data_to_serialize(request, data)

class FundReturnDailyResource(FundReturnResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnDaily.objects.all()

class FundReturnDailyResource2(FundReturnResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnDaily.objects.all()

class FundReturnMonthlyResource(FundReturnResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnMonthly.objects.all()


class FundReturnMonthlyResource2(FundReturnResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnMonthly.objects.all()


class FundReturnMonthlyResource3(FundReturnResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnMonthly.objects.all()

class HoldingResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Holding.objects.all()

class HoldingDailyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingDaily.objects.all()

class HoldingMonthlyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingMonthly.objects.all()
        

    def alter_list_data_to_serialize(self, request, data):            
    
        fund = request.GET.get('holding__fund', False)
        year = request.GET.get('value_date__year', False)
        month = request.GET.get('value_date__month', False)
        performance = request.GET.get('performance', False) 
        
        # W2 - Holding Performance Bar
        if performance and year and month and fund:
            
            # Get the weight of the holding from PositionMonthly
            pos = PositionMonthly.objects.filter(fund=fund, 
                value_date__year=year, value_date__month=month). \
                select_related('holding')
            
            new_data = []
            for i, d in enumerate(data['objects']):
                d.data['weight'] = 0
                d.data['weighted_perf'] = 0
                for p in pos:
                    if d.data['holding__name'] == p.holding.name:
                        d.data['weight'] = p.weight
                        d.data['weighted_perf'] = d.data['monthlyreturn'] * p.weight
        
            
        return super(HoldingMonthlyResource, self) \
                .alter_list_data_to_serialize(request, data)

class HoldingDepositResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingDeposit.objects.all()

class HoldingEtfResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingEtf.objects.all()

class HoldingEquityResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingEquity.objects.all()

class HoldingFixedIncomeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingFixedIncome.objects.all()

class HoldingForwardResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingForward.objects.all()

class HoldingFutureResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingFuture.objects.all()

class HoldingHedgeFundsResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingHedgeFund.objects.all()

class HoldingMutualFundResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingMutualFund.objects.all()

class HoldingOptionResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingOption.objects.all()

class HoldingWarrantResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingWarrant.objects.all()

class PositionDailyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = PositionDaily.objects.all()

class PositionMonthlyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = PositionMonthly.objects.all()

class TradeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.all()

