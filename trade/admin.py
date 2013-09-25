from django.contrib import admin
from trade.models import *
from holding.models import *
from alpheus.utils import create_modeladmin

class TradeAdmin(admin.ModelAdmin):
    change_form_template = 'admin/trade_change_form.html'
    actions = None

    def __init__(self, model, admin_site):
        self.fields = self.extra_fields + self.fields
        super(TradeAdmin, self).__init__(model, admin_site)


    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        fields = []

        for field in self.holding_fields:
            fields.append({
                'field': field,
                'name': field.replace('_', ' ').capitalize(),
                'value': '',
            })
        extra_context['holdings'] = fields

        return super(TradeAdmin, self).add_view(request, form_url,
                                                        extra_context)


    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        fields = []

        if object_id:
            trade = Trade.objects.get(pk=object_id)
            holding = Holding.objects.get(pk=trade.holding.id)

        for field in self.holding_fields:
            fields.append({
                'field': field,
                'name': field.replace('_', ' ').capitalize(),
                'value': getattr(holding, field),
            })
        extra_context['holdings'] = fields

        return super(TradeAdmin, self).change_view(request, object_id,
            form_url, extra_context)


class FundBaseAdmin(TradeAdmin):
    fields = (
        'holding',
        ('instruction_type', 'trade_date', 'settlement_date'),
        ('sub_red_cash_movement', 'instruction_date', 'dealing_date'),
        ('trade_no', 'desk', 'book'),
        ('bank_reference', 'memorandum_text'),
        ('no_of_units', 'trade_price_euro'), #, 'fxeuro'),
        ('percent_to_redeem', 'base_nav', 'euro_nav'),
        ('authorised_by', 'contract_note_received', 'proceed_date'),
        ('transaction_fees', 'counter_party', 'counter_party_trader'),
        ('delivery_fees', 'print_date', 'trade_slip_no'),
    )
    holding_fields = [
        'asset_class',
        'sector',
        'location',
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
        'redemption_fee12_percent',
        'redemption_fee24_percent',
        'redemption_fee36_percent',
        'no_of_units',
        'price_of_unit',
        'base_nav',
        'ave_purchase_price_base',
        'redemption_frequency',
        'redemption_notice',
        'max_redemption',
        'payment_days',
        'gate',
        'soft_lock_percent',
    ]


class FundAdmin(FundBaseAdmin):
    extra_fields = ('fund', )


class ClientFundAdmin(FundBaseAdmin):
    extra_fields = ('client', )


class EquityBaseAdmin(TradeAdmin):
    fields = (
        'holding',
        ('instruction_type', 'trade_date', 'settlement_date'),
        'buy_sell',
        ('trade_no', 'desk', 'book'),
        ('bank_reference', 'memorandum_text'),
        ('no_of_units', 'trade_price_base',),# 'fx_euro'),
        ('percent_to_redeem', 'corp_action_yes_no'),
        ('euro_nav', 'base_nav', ),
        ('transaction_fees', 'counter_party', 'counter_party_trader'),
        ('delivery_fees', 'print_date', 'trade_slip_no'),
    )
    holding_fields = [
        'asset_class',
        'sector',
        'sub_sector',
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
        'no_of_units',
        'price_of_unit',
        'base_nav',
        'ave_purchase_price_base',
        'etf_yes_no',
    ]


class FundEquityAdmin(EquityBaseAdmin):
    extra_fields = ('fund', )


class ClientEquityAdmin(EquityBaseAdmin):
    extra_fields = ('client', )


class OptionBaseAdmin(TradeAdmin):
    fields = (
        'holding',
        ('instruction_type', 'trade_date', 'settlement_date'),
        'buy_sell',
        ('trade_no', 'desk', 'book'),
        ('bank_reference', 'memorandum_text'),
        ('no_of_units', 'trade_price_base',),# 'fx_euro'),
        ('transaction_fees', 'counter_party', 'counter_party_trader'),
        ('delivery_fees', 'print_date', 'trade_slip_no'),
    )
    holding_fields = [
        'asset_class',
        'sector',
        'location',
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
        'no_of_units',
        'price_of_unit',
        'base_nav',
        'ave_purchase_price_base',
        'maturity',
        'strike',
        'multiplier',
        'put_call',
        'american_euro',
    ]


class FundOptionAdmin(OptionBaseAdmin):
    extra_fields = ('fund', )


class ClientOptionAdmin(OptionBaseAdmin):
    extra_fields = ('client', )


class FixedIncomeBaseAdmin(TradeAdmin):
    fields = (
        'holding',
        ('instruction_type', 'trade_date', 'settlement_date'),
        'buy_sell',
        ('trade_no', 'desk', 'book'),
        ('bank_reference', 'memorandum_text'),
        ('no_of_units', 'trade_price_base',),# 'fx_euro'),
        ('base_nav', 'euro_nav', ),
        ('transaction_fees', 'counter_party', 'counter_party_trader'),
        ('delivery_fees', 'print_date', 'trade_slip_no'),
    )
    holding_fields = [
        'asset_class',
        'sector',
        'location',
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
        'no_of_units',
        'price_of_unit',
        'base_nav',
        'ave_purchase_price_base',
        'maturity',
    ]


class FundFixedIncomeAdmin(FixedIncomeBaseAdmin):\
    extra_fields = ('fund', )


class ClientFixedIncomeAdmin(FixedIncomeBaseAdmin):
    extra_fields = ('client', )


class SidePocketBaseAdmin(TradeAdmin):
    fields = (
        'holding',
        ('instruction_type', 'trade_date', 'settlement_date'),
        'buy_sell',
        ('trade_no', 'desk', 'book'),
        ('bank_reference', 'memorandum_text'),
        ('valuation_base', 'valuation_euro'),
        ('various_base', 'various_euro'),
        ('distribution_base', 'distribution_euro'),
        ('transaction_fees', 'counter_party', 'counter_party_trader'),
        ('delivery_fees', 'print_date', 'trade_slip_no'),
    )
    holding_fields = [
        'asset_class',
        'sector',
        'location',
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
        'valuation',
    ]


class FundSidePocketAdmin(SidePocketBaseAdmin):
    extra_fields = ('fund', )


class ClientSidePocketAdmin(SidePocketBaseAdmin):
    extra_fields = ('client', )


class PrivateEquityBaseAdmin(TradeAdmin):
    fields = (
        'holding',
        ('instruction_type', 'trade_date', 'settlement_date'),
        'inflow_outflow_various_expense_valuation',
        ('trade_no', 'desk', 'book'),
        ('bank_reference', 'memorandum_text'),
        ('valuation_base', 'valuation_euro'),
        ('various_base', 'various_euro'),
        ('distribution_base', 'distribution_euro'),
        ('transaction_fees', 'counter_party', 'counter_party_trader'),
        ('delivery_fees', 'print_date', 'trade_slip_no'),
    )
    holding_fields = [
        'asset_class',
        'sector',
        'location',
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
        'valuation',
    ]


class FundPrivateEquityAdmin(PrivateEquityBaseAdmin):
    extra_fields = ('fund', )


class ClientPrivateEquityAdmin(PrivateEquityBaseAdmin):
    extra_fields = ('client', )


create_modeladmin(FundAdmin, name='Fund', model=Trade)
create_modeladmin(ClientFundAdmin, name='ClientFund', model=Trade)
create_modeladmin(FundEquityAdmin, name='FundEquity', model=Trade)
create_modeladmin(ClientEquityAdmin, name='ClientEquity', model=Trade)
create_modeladmin(FundOptionAdmin, name='FundOption', model=Trade)
create_modeladmin(ClientOptionAdmin, name='ClientOption', model=Trade)
create_modeladmin(FundFixedIncomeAdmin, name='FundFixedIncome', model=Trade)
create_modeladmin(ClientFixedIncomeAdmin, name='ClientFixedIncome', model=Trade)
create_modeladmin(FundSidePocketAdmin, name='FundSidePocket', model=Trade)
create_modeladmin(ClientSidePocketAdmin, name='ClientSidePocket', model=Trade)
create_modeladmin(FundPrivateEquityAdmin, name='FundPrivateEquity', model=Trade)
create_modeladmin(ClientPrivateEquityAdmin, name='ClientPrivateEquity', model=Trade)

admin.site.register(Trade)
