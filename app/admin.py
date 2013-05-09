from django.contrib import admin
from app.models import *
from mptt.admin import FeinCMSModelAdmin


class WidgetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key')

class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'widget_type', 'window', 'description',)


class WidgetInline(admin.TabularInline):
    model = Widget
    sortable_field_name = 'position'

class WindowAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'size_x', 'size_y', 'layout') #'access')

    inlines = [
        WidgetInline,
    ]

class MenuAdmin(FeinCMSModelAdmin):
    list_display = ('children', 'page')

class PageAdmin(FeinCMSModelAdmin):
    pass

class PageWindowAdmin(admin.ModelAdmin):
    pass

class FundPerformanceMonthlyAdmin(admin.ModelAdmin):
    list_display = ('fund', 'value', 'year', 'month')

class FundPerformanceYearlyAdmin(admin.ModelAdmin):
    list_display = ('fund', 'year', 'si', 'ytd')

class HoldingAdmin(admin.ModelAdmin):
    pass

class CurrencyAdmin(admin.ModelAdmin):
    pass

class CountryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(FundPerformanceMonthly, FundPerformanceMonthlyAdmin)
admin.site.register(FundPerformanceYearly, FundPerformanceYearlyAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(CounterParty)
admin.site.register(WidgetType, WidgetTypeAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Window, WindowAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageWindow, PageWindowAdmin)
admin.site.register(Fund)
admin.site.register(FundType)
