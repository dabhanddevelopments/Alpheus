from django.contrib import admin
from v2.models import *
from django import forms
from django.forms import Textarea

class FundBaseAdmin(admin.ModelAdmin):
    actions = None

class FundAdmin(FundBaseAdmin):
    class Media:
        css = {
             'all': ('fund_form.css',) #change size of left td's
        }

    fields = (
        ('name', 'group'), 
        'description',
        ('currency', 'asset_class'),
        ('country_issue', 'country_risk'),
        ('region_1', 'region_2'),
        'region_3', 
        ('benchpeer', 'sec_bench'),
        ('administrator', 'custodian'),
        ('manager', 'auditor'),
        ('active', 'estimate_required'),
    )
    
    # change description into a textarea
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(FundAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description':
            formfield.widget = forms.Textarea()
        return formfield

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'short_name']
    list_display = ('name', 'short_name')
    
    
admin.site.register(FundStyle)
admin.site.register(Fund, FundAdmin)
admin.site.register(Currency)
admin.site.register(AlpheusGroup)
admin.site.register(Auditor)
admin.site.register(Administrator)
admin.site.register(Custodian)
admin.site.register(Country, CountryAdmin)
#admin.site.register(Classification)
#admin.site.register(Administrator, AdministratorAdmin)
#admin.site.register(Auditor, AuditorAdmin)
#admin.site.register(Custodian, CustodianAdmin)
#admin.site.register(CounterParty)
#admin.site.register(CounterPartyTrader)
#admin.site.register(Alarm)
