from django.contrib import admin
from fund.models import *

class FundBaseAdmin(admin.ModelAdmin):
    actions = None

class FundAdmin(FundBaseAdmin):
    fields = (
        'name', 'classification', 'user', 'currency', 'description',
        ('custodian', 'custodian_management_fee', 'custodian_performance_fee'),
        ('administrator', 'administrator_fee'),
        ('auditor', 'auditor_fee'),
        'subscription_frequency',
        'redemption_frequency',
        'management_fee',
        'performance_fee',
        'benchmark',
    )
    filter_horizontal = ['benchmark']


class ClassificationAdmin(FundBaseAdmin):
    fields = ('name', 'asset_class')


class FxHedgeAdmin(FundBaseAdmin):
    fields = (
        'fund', 'client',
        ('trade_date', 'settlement_date'),
        ('currency', 'buy_sell', 'amount_base'), #, 'fx_euro'),
        'amount_euro',
        ('fx_fees', 'fx_fees_payable'),
        ('forward_fx_fees', 'forward_fx_fees_payable'),
    )


class DepositAdmin(FundBaseAdmin):
    fields = (
        'fund', 'client',
        ('trade_date', 'expiration_date'),
        ('currency', 'amount_base', 'amount_euro'), #, 'fx_euro'),
        ('deposit_interest_percent', 'deposit_interest_received_base')
    )

admin.site.register(CurrencyPosition)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(FxHedge, FxHedgeAdmin)
admin.site.register(FxRate)
admin.site.register(Fund, FundAdmin)
#admin.site.register(FundType)
admin.site.register(FundHistory)
admin.site.register(Classification, ClassificationAdmin)
