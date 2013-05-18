from django.contrib import admin
from app.models import *
from mptt.admin import FeinCMSModelAdmin


class WidgetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key')

class WidgetParamAdmin(admin.ModelAdmin):
    pass

class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'widget_type', 'window', 'description',)
    filter_horizontal = ['widget_param']


class WidgetInline(admin.TabularInline):
    model = Widget
    sortable_field_name = 'position'

class WindowAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'size_x', 'size_y', 'layout') #'access')

    inlines = [
        WidgetInline,
    ]

class MenuAdmin(FeinCMSModelAdmin):
    list_display = ('children', 'page', 'fund')

class PageAdmin(FeinCMSModelAdmin):
    pass

class PageWindowAdmin(admin.ModelAdmin):
    pass

class FundPerfDailyAdmin(admin.ModelAdmin):
    list_display = ('fund', 'holding', 'value', 'date')

class FundPerfMonthlyAdmin(admin.ModelAdmin):
    list_display = ('fund', 'holding_group', 'year', 'month')

class FundPerfYearlyAdmin(admin.ModelAdmin):
    list_display = ('fund', 'holding_group', 'year', 'si', 'ytd')

class HoldingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'holding_group')

class HoldingAdmin(admin.ModelAdmin):
    pass

class CurrencyAdmin(admin.ModelAdmin):
    pass

class CountryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(HoldingCategory, HoldingCategoryAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(CounterParty)
admin.site.register(WidgetType, WidgetTypeAdmin)
admin.site.register(WidgetParam, WidgetParamAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Window, WindowAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageWindow, PageWindowAdmin)
admin.site.register(Trade)
admin.site.register(TradeType)
admin.site.register(Fund)
admin.site.register(FundType)
admin.site.register(FundPerfDaily, FundPerfDailyAdmin)
admin.site.register(FundPerfMonthly, FundPerfMonthlyAdmin)
admin.site.register(FundPerfYearly, FundPerfYearlyAdmin)
admin.site.register(Fee)
admin.site.register(PurchaseSale)
admin.site.register(FundBench)
admin.site.register(FundBenchHist)
