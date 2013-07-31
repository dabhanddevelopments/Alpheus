from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
#from resources.api import api
#from resources.widgets import widget
from app import views
from fund import views as fund
from holding import views as holding
from client import views as client

from fund.resources import *
from holding.resources import *
from client.resources import *
from comparative.resources import *

admin.autodiscover()


from django.conf.urls.defaults import *
from tastypie.api import Api

api = Api(api_name="api")
from app.resources import *

# fund
api.register(FundResource())
api.register(FundHistoryResource())
api.register(FundValuationResource())
api.register(CurrencyPositionResource())
api.register(FxHedgeResource())
api.register(FxRateResource())
api.register(FundClassificationResource())

# holding
api.register(HoldingResource())
api.register(HoldingHistoryResource())
api.register(HoldingValuationResource())
api.register(BreakdownResource())
api.register(CountryBreakdownResource())
api.register(CategoryResource())
api.register(TradeResource())
api.register(AlpheusSubscriptionResource())

# client
api.register(ClientResource())
api.register(ClientHistoryResource())
api.register(SubscriptionRedemptionResource())

# app
api.register(ImportResource())
api.register(CurrencyResource())
api.register(InfoResource())
api.register(UserResource())
api.register(WidgetsResource())
api.register(LoggedInResource())
api.register(MenuResource())
api.register(MenuParentItemsResource())
api.register(PageResource(),canonical=True)
api.register(PageWindowResource(),canonical=True)

# comparative
api.register(BenchmarkResource())
api.register(BenchmarkHistoryResource())
api.register(PeerResource())
api.register(PeerHistoryResource())

urlpatterns = patterns('',
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^$', views.index, name='index'),

    url(r'^api/holding-performance-benchmark/$', holding.performancebenchmark),
    #url(r'^api/holding-reconciliation/$', holding.reconciliation),
    url(r'^api/holding-returnhistogram/$', holding.returnhistogram),
    url(r'^api/holding-correlation/$', holding.correlation),
    url(r'^api/holding-negativemonths-table/$', holding.negativemonthstable),
    url(r'^api/holding-negativemonths-graph/$', holding.negativemonthsgraph),
    url(r'^api/holding-best-worst/$', holding.bestworst),
    url(r'^api/holding-returns/$', holding.returns),

    #url(r'^api/client-reconciliation/$', client.reconciliation),
    url(r'^api/client-returnhistogram/$', client.returnhistogram),
    url(r'^api/client-correlation/$', client.correlation),
    url(r'^api/client-negativemonths-table/$', client.negativemonthstable),
    url(r'^api/client-negativemonths-graph/$', client.negativemonthsgraph),
    url(r'^api/client-best-worst/$', client.bestworst),
    url(r'^api/client-returns/$', client.returns),

    url(r'^api/fund-best-worst/$', fund.bestworst),
    url(r'^api/fund-returns/$', fund.returns),
    url(r'^api/fund-performance-benchmark/$', fund.performancebenchmark),
    url(r'^api/fund-reconciliation/$', fund.reconciliation),
    url(r'^api/fund-returnhistogram/$', fund.returnhistogram),
    url(r'^api/fund-correlation/$', fund.correlation),
    url(r'^api/fund-negativemonths-table/$', fund.negativemonthstable),
    url(r'^api/fund-negativemonths-graph/$', fund.negativemonthsgraph),
    url(r'^api/fund-subredtable/$', fund.subredtable),
    url(r'^api/fund-currencyhedge/$', fund.currencyhedge),
    url(r'^api/fund-grossasset1/$', fund.grossasset1),
    url(r'^api/fund-grossasset2/$', fund.grossasset2),
    url(r'^api/fund-grossasset3/$', fund.grossasset3),
    url(r'^api/fund-grossasset4/$', fund.grossasset4),
    url(r'^api/fund-grossasset5/$', fund.grossasset5),
    url(r'^api/fund-grossasset6/$', fund.grossasset6),

    url(r'admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    (r'', include(api.urls)),
    )

