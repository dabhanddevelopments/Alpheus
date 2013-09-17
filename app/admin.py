from django.contrib import admin
from django.http import HttpResponseRedirect
from app.models import *
from mptt.admin import FeinCMSModelAdmin


class WidgetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key')

class WidgetParamAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'used_on_window')
    list_filter = ('key', 'value')
    search_fields = ('key', 'value')
    list_editable = ('value', )

class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'widget_type', 'window', 'description', 'columns')
    filter_horizontal = ['widget_param']
    list_editable = ['key']
    list_filter = ['widget_type', 'widget_param', 'key']
    search_fields = ('name', 'key', 'description', 'columns')
    save_as = True


class WidgetInline(admin.TabularInline):
    model = Widget
    sortable_field_name = 'position'
    exclude = ('widget_param', 'description', 'column_width')
    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"

class WindowAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'size_x', 'size_y', 'layout') #'access')
    save_as = True
    inlines = [
        WidgetInline,
    ]

class MenuAdmin(FeinCMSModelAdmin):
    list_display = ('children', 'page', 'fund')

    def response_change(self, request, obj):
        #if not '_continue' in request.POST:
        #    return HttpResponseRedirect("/asdf")
        #else:
        return super(MenuAdmin, self).response_change(request, obj)

class PageAdmin(FeinCMSModelAdmin):
    pass

class PageWindowAdmin(admin.ModelAdmin):
    list_display = ('page', 'window', 'user', 'col', 'row')
    list_filter = ['page__title']


class CurrencyAdmin(admin.ModelAdmin):
    pass

class CountryAdmin(admin.ModelAdmin):
    pass

class CustodianAdmin(admin.ModelAdmin):
    fields = ('name', 'contact_name', 'contact_number')

class AuditorAdmin(admin.ModelAdmin):
    fields = ('name', 'contact_name', 'contact_number')

class AdministratorAdmin(admin.ModelAdmin):
    fields = ('name', 'contact_name', 'contact_number')


admin.site.register(WidgetType, WidgetTypeAdmin)
admin.site.register(WidgetParam, WidgetParamAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Window, WindowAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageWindow, PageWindowAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Classification)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Auditor, AuditorAdmin)
admin.site.register(Custodian, CustodianAdmin)
admin.site.register(CounterParty)
admin.site.register(CounterPartyTrader)
admin.site.register(Alarm)
"""
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(HoldingCategory, HoldingCategoryAdmin)


admin.site.register(Trade)
admin.site.register(TradeType)
admin.site.register(Fund)
admin.site.register(FundType)
admin.site.register(FundPerf, FundPerfDailyAdmin)
admin.site.register(FundPerfMonth, FundPerfMonthlyAdmin)
admin.site.register(HoldPerf)
admin.site.register(HoldPerfMonth)
admin.site.register(Fee)
admin.site.register(PurchaseSale)
admin.site.register(FundBench)
admin.site.register(FundBenchHist)
admin.site.register(FxHedge)

admin.site.register(Client)
admin.site.register(ClientPerfMonth)
admin.site.register(CurrencyPositionMonth)
admin.site.register(SubscriptionRedemption)
admin.site.register(CountryBreakdown)
"""
