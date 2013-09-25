from django.contrib import admin
from client.models import *

"""
from django import forms
from django.contrib import admin
from myapp.models import Person

class SubscriptionRedemptionForm(forms.ModelForm):

    class Meta:
        model = SubscriptionRedemption

class PersonAdmin(admin.ModelAdmin):
    exclude = ['age']
    form = PersonForm
"""

class SubscriptionRedemptionAdmin(admin.ModelAdmin):
    list_display = ['client', 'fund', 'instruction_type', 'sub_red_switch', 'instruction_date', 'dealing_date', 'redemption_date']
    search_fields = ['client', 'fund']
    list_filter = ['client', 'fund', 'instruction_type', 'sub_red_switch']
    actions = None
    fields = (
        'instruction_type', 'sub_red_switch',
        ('fund',), #j 'destination_fund'),
        ('trade_date', 'instruction_date'),
        ('dealing_date', 'settlement_date'),
        'client',
        ('no_of_units', 'sub_red_price_base'),
        ('sub_red_base_nav', 'sub_red_euro_nav'),
        ('percent_released', 'redemption_date'),
    )

class ClientAdmin(admin.ModelAdmin):
    fields = (
        ('first_name', 'last_name'),
        'core_non_core', 'objective', 'account_number'
    )

admin.site.register(Client, ClientAdmin)
admin.site.register(ClientHistory)
admin.site.register(SubscriptionRedemption, SubscriptionRedemptionAdmin)
