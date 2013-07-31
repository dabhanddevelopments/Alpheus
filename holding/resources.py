from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.api import Api

from holding.models import *
from alpheus.base_resources import MainBaseResource, TreeBaseResource
from app.resources import CurrencyResource
from fund.resources import FundResource
from client.resources import ClientResource


class CategoryResource(MainBaseResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'holding-category'
        filtering = {
            "key": ALL,
            'group': ALL,
        }

class HoldingResource(MainBaseResource):
    fund = fields.ManyToManyField(FundResource, 'fund', related_name='holding_fund')
    client = fields.ManyToManyField(ClientResource, 'client', \
                                    related_name='holding_client')
    currency = fields.ForeignKey(CurrencyResource, 'currency')
    category = fields.ForeignKey(CategoryResource, 'category')
    sector = fields.ForeignKey(CategoryResource, 'sector', \
                                     related_name='sec')
    sub_sector = fields.ForeignKey(CategoryResource, 'sub_sector', \
                                        related_name='sub_sec')
    location = fields.ForeignKey(CategoryResource, 'location', \
                                                related_name='loc')
    investment_type = fields.ForeignKey(CategoryResource, 'investment_type', \
                                                            related_name='inv')
    asset_class = fields.ForeignKey(CategoryResource, 'asset_class', \
                                                    related_name='ass')

    class Meta(MainBaseResource.Meta):
        queryset = Holding.objects.all()
        resource_name = 'holding'
        filtering = {
            "value_date": ALL,
            "asset_class": ALL_WITH_RELATIONS,
            "fund": ALL_WITH_RELATIONS,
            "client": ALL_WITH_RELATIONS,
            "date_type": ALL,
            "id": ALL,
        }


class HoldingHistoryResource(MainBaseResource):
    #fund = fields.ForeignKey(FundResource, "fund")
    holding = fields.ForeignKey(HoldingResource, "holding")


    class Meta(MainBaseResource.Meta):
        queryset = HoldingHistory.objects.all()
        resource_name = 'holding-history'
        ordering = ['value_date', 'dealing_date', 'weight', 'performance']
        filtering = {
            #"fund": ALL,
            "holding": ALL_WITH_RELATIONS,
            "value_date": ALL,
            "date_type": ALL,
        }

class HoldingValuationResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    holding = fields.ForeignKey(HoldingResource, 'holding')
    category = fields.ForeignKey(CategoryResource, 'category', null=True)

    class Meta(MainBaseResource.Meta):
        queryset = HoldingHistory.objects.all()
        resource_name = 'holding-valuation'
        allowed_fields = ['valuation',  'holding__name', 'net_movement', 'value_date', 'delta_valuation', 'delta_flow', ]
        filtering = {
            "fund": ALL,
            "value_date": ALL,
            "category": ALL_WITH_RELATIONS,
            "date_type": ALL,
        }
        ordering = ['holding__name', 'value_date']

    def alter_list_data_to_serialize(self, request, data):

        import calendar

        fields = []
        def set_fields(field, group, extra_fields = []):
            dic = {'type': field.replace('_', ' ').title(), 'group': group}
            for row in data['objects']:
                if row.data['holding__name'] == group:
                    month = row.data['value_date'].month
                    month_name = calendar.month_abbr[month].lower()
                    dic[month_name] = row.data[field]
                    for extra_field in extra_fields:
                        dic[extra_field] = row.data[extra_field]
            fields.append(dic)

        holdings = set([row.data['holding__name'] for row in data['objects']])
        extra_fields = ['delta_valuation', 'delta_flow']

        for holding in holdings:
            set_fields('valuation', holding, extra_fields)
            set_fields('net_movement', holding)

        columns = ['type'] + self.get_month_list() + ['delta_valuation', 'delta_flow']
        return {
            'columns': self.set_columns(request, columns),
            'rows': fields,
        }



# will be used later. atm parent class for country breakdown
class BreakdownResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    category = fields.ForeignKey(CategoryResource, 'category')

    class Meta(MainBaseResource.Meta):
        queryset = Breakdown.objects.all()
        resource_name = 'holding-breakdown'
        filtering = {
            "fund": ALL,
            "value_date": ALL,
            "category": ALL_WITH_RELATIONS,
            "date_type": ALL,
        }


class CountryBreakdownResource(BreakdownResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    category = fields.ForeignKey(CategoryResource, 'category')

    class Meta(BreakdownResource.Meta):
        queryset = CountryBreakdown.objects.all()
        resource_name = 'country-breakdown'
        filtering = {
            "fund": ALL,
            "category": ALL_WITH_RELATIONS,
            "value_date": ALL,
            "date_type": ALL,
        }

class TradeResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund', null=True)
    client = fields.ForeignKey(ClientResource, 'client', null=True)
    currency = fields.ForeignKey(CurrencyResource, 'currency')
    holding = fields.ForeignKey(HoldingResource, 'holding')

    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.all()
        resource_name = 'trade'
        filtering = {
            "fund": ALL,
            "value_date": ALL,
            "trade_date": ALL,
            "holding": ALL_WITH_RELATIONS,
        }




class AlpheusSubscriptionResource(MainBaseResource):
    holding = fields.ForeignKey(FundResource, 'holding')
    client = fields.ForeignKey(ClientResource, 'client')

    class Meta(MainBaseResource.Meta):
        queryset = HoldingHistory.months.filter(client__isnull=False)
        resource_name = 'alpheus-subscription'
        filtering = {
            "fund": ALL,
            "value_date": ALL,
            "date_type": ALL,
        }
        ordering = ['value_date']

    def alter_list_data_to_serialize(self, request, data):

        holdings = set([row.data['holding__name'] for row in data['objects']])

        dic = {}
        lis = []
        for row in data['objects']:
            for holding in holdings:
                if row.data['holding__name'] == holding:
                    key = holding.replace(' ', '_').lower()
                    dic['euro_nav' + key] = row.data['euro_nav']
                    dic['no_of_units' + key] = row.data['no_of_units']
            dic['client__first_name'] = row.data['client__first_name']
            lis.append(dic)



        return lis


