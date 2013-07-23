from django.contrib import admin
from holding.models import *


admin.site.register(Category)
admin.site.register(Holding)
admin.site.register(HoldingHistory)
admin.site.register(CountryBreakdown)
admin.site.register(Breakdown)
admin.site.register(Trade)


