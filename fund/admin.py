from django.contrib import admin
from fund.models import *


admin.site.register(CurrencyPosition)
admin.site.register(FxHedge)
admin.site.register(FxRate)
admin.site.register(Fund)
#admin.site.register(FundType)
admin.site.register(FundHistory)
admin.site.register(Classification)
