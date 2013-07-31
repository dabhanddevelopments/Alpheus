from django.contrib import admin
from holding.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'group']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Holding)
admin.site.register(HoldingHistory)
admin.site.register(CountryBreakdown)
admin.site.register(Breakdown)
admin.site.register(Trade)


