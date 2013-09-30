from django.contrib import admin
from holding.models import *
from alpheus.utils import create_modeladmin
from django.forms import TextInput, Textarea
from alpheus.admin import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'group']


class HoldingAdmin(admin.ModelAdmin):
    actions = None

    def __init__(self, model, admin_site):
        self.fields = self.extra_fields + self.fields
        super(HoldingAdmin, self).__init__(model, admin_site)



class FundBaseAdmin(FundMixin, HoldingAdmin):
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

class FundAdmin(FundBaseAdmin):
    extra_fields = ('fund', )


class ClientFundAdmin(FundBaseAdmin):
    extra_fields = ('client', )


class EquityBaseAdmin(EquityMixin, HoldingAdmin):
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

class FundEquityAdmin(EquityBaseAdmin):
    extra_fields = ('fund', )


class ClientEquityAdmin(EquityBaseAdmin):
    extra_fields = ('client', )


class OptionBaseAdmin(OptionMixin, HoldingAdmin):
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


class FundOptionAdmin(OptionBaseAdmin):
    extra_fields = ('fund', )


class ClientOptionAdmin(OptionBaseAdmin):
    extra_fields = ('client', )


class FixedIncomeBaseAdmin(FixedIncomeMixin, HoldingAdmin):
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


class FundFixedIncomeAdmin(FixedIncomeBaseAdmin):
    extra_fields = ('fund', )


class ClientFixedIncomeAdmin(FixedIncomeBaseAdmin):
    extra_fields = ('client', )


class SidePocketBaseAdmin(SidePocketMixin, HoldingAdmin):
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


class FundSidePocketAdmin(SidePocketBaseAdmin):
    extra_fields = ('fund', )


class ClientSidePocketAdmin(SidePocketBaseAdmin):
    extra_fields = ('client', )



class PrivateEquityBaseAdmin(PrivateEquityMixin, HoldingAdmin):
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


class FundPrivateEquityAdmin(PrivateEquityBaseAdmin):
    extra_fields = ('fund', )


class ClientPrivateEquityAdmin(PrivateEquityBaseAdmin):
    extra_fields = ('client', )


create_modeladmin(FundAdmin, name='Fund', model=Holding)
create_modeladmin(ClientFundAdmin, name='ClientFund', model=Holding)
create_modeladmin(FundEquityAdmin, name='FundEquity', model=Holding)
create_modeladmin(ClientEquityAdmin, name='ClientEquity', model=Holding)
create_modeladmin(FundOptionAdmin, name='FundOption', model=Holding)
create_modeladmin(ClientOptionAdmin, name='ClientOption', model=Holding)
create_modeladmin(FundFixedIncomeAdmin, name='FundFixedIncome', model=Holding)
create_modeladmin(ClientFixedIncomeAdmin, name='ClientFixedIncome', model=Holding)
create_modeladmin(FundSidePocketAdmin, name='FundSidePocketHolding', model=Holding)
create_modeladmin(ClientSidePocketAdmin, name='ClientSidePocketHolding', model=Holding)
create_modeladmin(FundPrivateEquityAdmin, name='FundPrivateEquity', model=Holding)
create_modeladmin(ClientPrivateEquityAdmin, name='ClientPrivateEquity', model=Holding)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Holding)
admin.site.register(HoldingHistory)
admin.site.register(CountryBreakdown)
admin.site.register(Breakdown)


