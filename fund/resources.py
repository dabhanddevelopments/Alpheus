from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.api import Api

from fund.models import *
from app.resources import *
from comparative.resources import BenchmarkResource
from alpheus.base_resources import MainBaseResource, TreeBaseResource




class FundClassificationResource(MainBaseResource):

    class Meta:
        queryset = Classification.objects.all()
        resource_name = 'fund/classification'


class FundTypeResource(MainBaseResource):

    class Meta(MainBaseResource.Meta):
        queryset = FundType.objects.all()



class FundResource(MainBaseResource):
    classification = fields.ForeignKey(FundClassificationResource, "classification")
    benchmark = fields.ManyToManyField(BenchmarkResource, "benchmark")

    fund_type = fields.ForeignKey(FundTypeResource,'fund_type')
    custodian = fields.ForeignKey(CustodianResource, 'custodian')
    auditor = fields.ForeignKey(AuditorResource, 'auditor')
    administrator =  fields.ForeignKey(AdministratorResource, 'administrator')
    manager = fields.ForeignKey(ManagerResource, 'manager')

    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        resource_name = 'fund'
        filtering = {
            'id': ALL,
            'value_date': ALL,
            'benchmark': ALL_WITH_RELATIONS,
            'custodian': ALL_WITH_RELATIONS,
        }

class FundHistoryResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, "fund")

    class Meta(MainBaseResource.Meta):
        queryset = FundHistory.objects.all()
        resource_name = 'fund-history'
        ordering = ['value_date']
        filtering = {
            'value_date': ALL,
            'date_type': ALL,
            'fund': ALL,
        }


class CurrencyPositionResource(MainBaseResource):
    currency = fields.ForeignKey(CurrencyResource, "currency")
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta:
        queryset = CurrencyPosition.objects.all()
        resource_name = 'currency-position'
        filtering = {
            "fund": ALL,
            "value_date": ALL,
        }

class FxHedgeResource(MainBaseResource):
    currency = fields.ForeignKey(CurrencyResource, "currency")
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta:
        queryset = FxHedge.objects.all()
        resource_name = 'fxhedge'
        filtering = {
            "fund": ALL,
            "value_date": ALL,
        }

class FxRateResource(MainBaseResource):
    currency = fields.ForeignKey(CurrencyResource, "currency")

    class Meta:
        queryset = FxRate.objects.all()
        resource_name = 'fxrate'


class FundValuationResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')

    class Meta(MainBaseResource.Meta):
        queryset = FundHistory.objects.all()
        resource_name = 'fund-valuation'
        allowed_fields = [
            'net_movement',
            'valuation',
            'value_date',
            'delta_valuation',
            'delta_flow',
            'inflow_euro',
            'inflow_dollar',
            'outflow_euro',
            'outflow_dollar'
        ]
        filtering = {
            "fund": ALL,
            "value_date": ALL,
        }
        ordering = ['value_date']

    def alter_list_data_to_serialize(self, request, data):

        import calendar

        fields = []
        def set_fields(field, name, group):
            extra_fields = ['delta_valuation', 'delta_flow']
            dic = {'type': name, 'group': group}
            for row in data['objects']:
                month = row.data['value_date'].month
                month_name = calendar.month_abbr[month].lower()
                dic[month_name] = row.data[field]
                for extra_field in extra_fields:
                    dic[extra_field] = row.data[extra_field]
            fields.append(dic)

        set_fields('valuation', 'Valuation', 'Total')
        set_fields('net_movement', 'Net Movement', 'Total')
        set_fields('inflow_euro', 'Euro', 'Inflow')
        set_fields('inflow_dollar', 'US Dollar', 'Inflow')
        set_fields('outflow_euro', 'Euro', 'Outflow')
        set_fields('outflow_euro', 'US Dollar', 'Outflow')

        columns = ['type'] + self.get_month_list() + ['delta_valuation', 'delta_flow']
        return {
            'columns': self.set_columns(request, columns),
            'rows': fields,
        }






"""
class FundByTypeResource(MainBaseResource):
    funds = fields.ToManyField(FundResource, "fund", full=True)

    class Meta(MainBaseResource.Meta):
        queryset = FundType.objects.all()

class FundNameResource(MainBaseResource):

    fund_type = fields.ForeignKey(FundTypeResource, "fund_type")

    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
        fields = ['name', 'fund_type']
"""
