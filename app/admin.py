from django.contrib import admin
from app.models import *
from mptt.admin import FeinCMSModelAdmin


class WidgetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key')

class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'widget_type', 'size_x', 'size_y', 'description')

class MenuAdmin(FeinCMSModelAdmin):
    list_display = ('children', 'page')

class PageAdmin(FeinCMSModelAdmin):
    pass

class PageWidgetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Menu, MenuAdmin)
admin.site.register(CounterParty)
admin.site.register(WidgetType, WidgetTypeAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageWidget, PageWidgetAdmin)
admin.site.register(Fund)
admin.site.register(FundType)
