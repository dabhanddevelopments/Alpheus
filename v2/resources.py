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
from operator import itemgetter
from django.db.models import Sum

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
  

    def alter_list_data_to_serialize(self, request, data):   
          
        fund = request.GET.get('fund', False)  
        
        # W15 - Fund Summary
        if request.GET.get('summary', False):
        
            fees = FundFee.objects.filter(fund=fund).select_related('fee').only('fee__name', 'fee__formula')
            
            data['objects'] = []
            new_data = {}
            for fee in fees:
            
                if fee.fee.formula == None:
                    formula = 'n/a'
                else:
                    formula = fee.fee.formula
                    
                new_data = {
                    'name': fee.fee.name,
                    'formula': formula
                }
                new_obj = self.build_bundle(data = new_data)
                data['objects'].insert(0, new_obj)
                
        return super(FundFeeResource, self) \
                .alter_list_data_to_serialize(request, data)
                
                
class FundFeeAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundFeeAudit.objects.all()


class FundPositionAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundPositionAudit.objects.all()

class FundResource(MainBaseResource):
    benchpeer = fields.ForeignKey(BenchPeer, "benchpeer")
    
    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
    

    def alter_detail_data_to_serialize(self, request, data):   
    
        # W15 - Fund Summary
        if request.GET.get('summary', False):
        
            try:
                first = FundReturnDaily.objects.filter(fund=data.data['id']) \
                    .only('value_date', 'nav').order_by('value_date')[0]
            except IndexError:
                try:
                    first = FundReturnMonthly.objects.filter(fund=data.data['id']) \
                        .only('value_date', 'nav').order_by('value_date')[0]
                except IndexError:
                    return
               
            try: 
                last = FundReturnDaily.objects.filter(fund=data.data['id']) \
                    .only('value_date', 'nav').order_by('-value_date')[0]
            except IndexError:
                last = FundReturnMonthly.objects.filter(fund=data.data['id']) \
                   .only('value_date', 'nav').order_by('-value_date')[0]
                
            flows = FundReturnMonthly.objects.aggregate(Sum('inflow'), Sum('outflow'))
            
            data.data['launch_date'] = first.value_date
            data.data['start_nav'] = first.nav
            data.data['end_nav'] = last.nav
            data.data['net_flow'] = flows['inflow__sum'] + flows['outflow__sum']
                
        return super(FundResource, self) \
                .alter_detail_data_to_serialize(request, data)
                

class FundPeerResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    class Meta(MainBaseResource.Meta):
        queryset = FundPeer.objects.all()
        
class FundCharAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundCharAudit.objects.all()


class FundReturnResource(MainBaseResource):

    def alter_list_data_to_serialize(self, request, data):   
    
        fund = request.GET.get('fund', False)      
    
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
    holding = fields.ForeignKey(HoldingResource, 'holding')
    class Meta(MainBaseResource.Meta):
        queryset = HoldingMonthly.objects.all()

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

class HoldingPositionDailyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingPositionDaily.objects.all()

class HoldingPositionMonthlyResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    
    class Meta(MainBaseResource.Meta):
        queryset = HoldingPositionMonthly.objects.all()
        

    def alter_list_data_to_serialize(self, request, data):            
    
        fund = request.GET.get('fund', False)
        year = request.GET.get('value_date__year', False)
        month = request.GET.get('value_date__month', False)
        performance = request.GET.get('performance', False) 
        
        # W2 - Holding Performance Bar & W7 Holding NAV
        # Get monthlyreturn from HoldingMonthly (only utilized in W2)
        # and the weight of the prior month to calculate the average weight
        if performance and year and month and fund:
        
            
            hm = HoldingMonthly.objects.filter(
                value_date__year=year, value_date__month=month). \
                select_related('holding').only('holding__name', 'monthlyreturn')
                
            if int(month) == 1:
                prior_year = int(year) - 1
                prior_month = 12
            else:
                prior_year = year
                prior_month = int(month) - 1
                
            prior_pos = HoldingPositionMonthly.objects.filter(
                value_date__year=prior_year, value_date__month=prior_month,
                fund=fund). \
                select_related('holding').only('holding__name', 'weight')
                
            pos = data['objects']
            data['objects'] = [] # delete old data
            new_data = {}
            
            # set the average weight for the current month
            for i, p in enumerate(pos):
                for h in hm:
                    if p.data['holding__name'] == h.holding.name:
                        
                        name = h.holding.name
                        
                        average_weight = p.data['weight']
                            
                        if average_weight >= 0:
                        
                            new_data[name] = {
                                'weighted_perf': p.data['weight'] * h.monthlyreturn,
                                'average_weight': average_weight, 
                                'monthlyreturn': h.monthlyreturn,
                                'holding__name': p.data['holding__name'],
                            }
                            
            # update the average weight for prior months (if exists)
            for i, p in enumerate(pos):
                for pp in prior_pos:
                    for h in hm:
                        if p.data['holding__name'] == h.holding.name and pp.holding.name == h.holding.name:
                        
                            name = h.holding.name
                            
                            if pp.weight > 0:
                                average_weight = p.data['weight'] + (pp.weight / 2)
                        
                                new_data[name]['average_weight'] = average_weight
                                
            # convert dictionary to a list of dictionaries
            sorted_data = []
            for i, new in new_data.iteritems():
                sorted_data.append(new)
             
            # sort by average weight
            new_data = sorted(sorted_data, key=itemgetter('average_weight')) 
            
            # insert new data
            for new in new_data:
                new_obj = self.build_bundle(data = new)
                data['objects'].insert(0, new_obj)
         
        return super(HoldingPositionMonthlyResource, self) \
                .alter_list_data_to_serialize(request, data)

class TradeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.all()

