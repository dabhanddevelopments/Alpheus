from django.contrib import admin
from holding.models import *
from alpheus.utils import create_modeladmin
from django.forms import TextInput, Textarea


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'group']


class HoldingAdmin(admin.ModelAdmin):
    pass


class FundHoldingAdmin(HoldingAdmin):
    fields = (
        ('name', 'no_of_units'),
        ('asset_class', 'price_of_unit'),
        ('sector', 'base_nav'),
        ('location', 'ave_purchase_price_base'),
        ('country', 'redemption_frequency'),
        ('currency', 'redemption_notice'),
        ('sec_id', 'max_redemption'),
        ('bloomberg_code', 'payment_days'),
        ('redemption_fee12_percent', 'gate'),
        ('redemption_fee24_percent', 'soft_lock_percent'),
        'redemption_fee36_percent',
    )


class EquityHoldingAdmin(HoldingAdmin):
    fields = (
        ('name', 'no_of_units'),
        ('asset_class', 'price_of_unit'),
        ('sector', 'base_nav'),
        ('sub_sector', 'ave_purchase_price_base'),
        ('location', 'etf_yes_no'),
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
    )


class OptionHoldingAdmin(HoldingAdmin):
    fields = (
        ('name', 'no_of_units'),
        ('asset_class', 'price_of_unit'),
        ('sector', 'base_nav'),
        ('location', 'ave_purchase_price_base'),
        ('country', 'maturity'),
        ('currency', 'strike'),
        ('sec_id', 'multiplier'),
        'bloomberg_code',
         ('put_call', 'american_euro'),
    )


class FixedIncomeHoldingAdmin(HoldingAdmin):
    fields = (
        ('name', 'no_of_units'),
        ('asset_class', 'price_of_unit'),
        ('sector', 'base_nav'),
        ('location', 'ave_purchase_price_base'),
        ('country', 'maturity'),
        'currency',
        'sec_id',
        'bloomberg_code',
    )


class SidePocketHoldingAdmin(HoldingAdmin):
    fields = (
        ('name', 'valuation'),
        'asset_class',
        'sector',
        'location',
        'country',
        'currency',
        'sec_id',
        'bloomberg_code',
    )


class TradeAdmin(admin.ModelAdmin):

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


class FundTradeAdmin(TradeAdmin):
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


class EquityTradeAdmin(TradeAdmin):
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


class OptionTradeAdmin(TradeAdmin):
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


class FixedIncomeTradeAdmin(TradeAdmin):
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


class SidePocketTradeAdmin(TradeAdmin):
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


class PrivateEquityTradeAdmin(TradeAdmin):
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
        'asset_class', 'sector', 'location', 'country', 'currency', 'sec_id',
        'bloomberg_code', 'redemption_fee12_percent', 'redemption_fee24_percent',
        'redemption_fee36_percent', 'no_of_units', 'price_of_unit',
        'base_nav', 'ave_purchase_price_base', 'redemption_frequency',
        'redemption_notice', 'max_redemption', 'payment_days', 'gate', 'soft_lock_percent',
    ]
    change_form_template = 'admin/trade_change_form.html'




create_modeladmin(FundHoldingAdmin, name='FundHolding', model=Holding)
create_modeladmin(EquityHoldingAdmin, name='EquityHolding', model=Holding)
create_modeladmin(OptionHoldingAdmin, name='OptionHolding', model=Holding)
create_modeladmin(FixedIncomeHoldingAdmin, name='FixedIncomeHolding', model=Holding)
create_modeladmin(SidePocketHoldingAdmin, name='SidePocketHolding', model=Holding)
create_modeladmin(SidePocketHoldingAdmin, name='PrivateEquityHolding', model=Holding)

create_modeladmin(FundTradeAdmin, name='FundTrade', model=Trade)
create_modeladmin(EquityTradeAdmin, name='EquityTrade', model=Trade)
create_modeladmin(OptionTradeAdmin, name='OptionTrade', model=Trade)
create_modeladmin(FixedIncomeTradeAdmin, name='FixedIncomeTrade', model=Trade)
create_modeladmin(SidePocketTradeAdmin, name='SidePocketTrade', model=Trade)
create_modeladmin(PrivateEquityTradeAdmin, name='PrivateEquityTrade', model=Trade)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Holding)
admin.site.register(HoldingHistory)
admin.site.register(CountryBreakdown)
admin.site.register(Breakdown)
admin.site.register(Trade)


