from django.contrib import admin
from app.models import *
from mptt.admin import FeinCMSModelAdmin


class WidgetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key')

class WidgetParamAdmin(admin.ModelAdmin):
    pass

class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'widget_type', 'window', 'description', 'v2')
    filter_horizontal = ['widget_param']
    list_editable = ['key']
    list_filter = ['widget_type']
    save_as = True


class WidgetInline(admin.TabularInline):
    model = Widget
    sortable_field_name = 'position'
    exclude = ('widget_param', 'description', 'column_width')

class WindowAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'size_x', 'size_y', 'layout') #'access')
    save_as = True
    inlines = [
        WidgetInline,
    ]

class MenuAdmin(FeinCMSModelAdmin):
    list_display = ('children', 'page', 'fund')

class PageAdmin(FeinCMSModelAdmin):
    pass

class PageWindowAdmin(admin.ModelAdmin):
    list_display = ('page', 'window', 'user', 'col', 'row')
    list_filter = ['page__title']


class CurrencyAdmin(admin.ModelAdmin):
    pass

class CountryAdmin(admin.ModelAdmin):
    pass


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
admin.site.register(Administrator)
admin.site.register(Auditor)
admin.site.register(Custodian)
admin.site.register(CounterParty)
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
