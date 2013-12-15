from tastypie import fields
from alpheus.base_resources import MainBaseResource
from v2.models import *
from alpheus.utils import fund_return_calculation

class AdministratorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Administrator.objects.all()

class AlarmResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Alarm.objects.all()

class GroupResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Group.objects.all()

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

class ClientFilenameResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = ClientFilename.objects.all()

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
    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        
    def alter_list_data_to_serialize(self, request, data):

        if self.y1 != False:

            fund = ''
            bench = ''
            for row in data['objects']:
                fund += str(row.data[self.y1]) + ', '
                bench += str(row.data[self.y2]) + ', '

            length = str(len(data['objects']))
            date = data['objects'][0].data[self.date]

            fund = fund_return_calculation(fund, date, length)
            bench = fund_return_calculation(bench, date, length)

            for row in data['objects']:
                for key, val in fund.iteritems():
                    if row.data[self.date].year == key.year and row.data[self.date].month == key.month:
                        row.data[self.y1] = val
                for key, val in bench.iteritems():
                    if row.data[self.date].year == key.year and row.data[self.date].month == key.month:
                        row.data[self.y2] = val

        return super(FundReturnMonthlyResource, self) \
                .alter_list_data_to_serialize(request, data)

class FundCharAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundCharAudit.objects.all()

class FundReturnDailyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnDaily.objects.all()

class FundEstimateResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundEstimate.objects.all()

class FundReturnMonthlyResource(MainBaseResource):
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

