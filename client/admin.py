from django.contrib import admin
from client.models import *


class SubscriptionRedemptionAdmin(admin.ModelAdmin):
    pass
    """
    fields = (
        'instruction_type', 'sub_red_switch',
        ('fund', 'destination_fund'),
        ('trade_date', 'instruction_date'),
        ('dealing_date', 'settlement_date'),
        'client',
        ('no_of_units', 'price')
    )
    """

class ClientAdmin(admin.ModelAdmin):
    fields = (
        ('first_name', 'last_name'),
        'core_non_core', 'objective', 'account_number'
    )

admin.site.register(Client, ClientAdmin)
admin.site.register(ClientHistory)
admin.site.register(SubscriptionRedemption, SubscriptionRedemptionAdmin)
