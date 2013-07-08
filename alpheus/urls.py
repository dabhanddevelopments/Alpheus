from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from resources.api import api
from resources.widgets import widget
from app import views

admin.autodiscover()


from django.conf.urls.defaults import *
from tastypie.api import Api
from api_example.resources import EntryResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EntryResource())

urlpatterns = patterns('',
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^$', views.index, name='index'),
    url(r'^check-nodes/$', views.check_nodes),
    url(r'^mainmenu/$', views.mainmenu),
    url(r'^api/widget/fundperfdatatable/$', views.fund_perf_data_table),
    url(r'^api/widget/fundallochistnav/$', views.fundallochistnav),
    url(r'^api/widget/fundperfbenchcomptable/$', views.fundperfbenchcomptable),
    url(r'^api/widget/fundperfbenchcompline/$', views.fundperfbenchcompline),
    url(r'^api/widget/fundbestworst/$', views.fundbestworst),
    url(r'^api/widget/fundreturnhistogram/$', views.fundreturnhistogram),
    url(r'^api/widget/fundcorrelationmatrix/$', views.fundcorrelationmatrix),
    url(r'^api/widget/holdcorrelationmatrix/$', views.holdcorrelationmatrix),
    url(r'^api/widget/fundnegativemonthstable/$', views.fundnegativemonthstable),
    url(r'^api/widget/fundnegativemonthsgraph/$', views.fundnegativemonthsgraph),
    url(r'^api/widget/fundnavreconciliation/$', views.fundnavreconciliation),
    url(r'^api/widget/subscriptionredemptionmonth/$', views.subscriptionredemptionmonth),
    url(r'^api/widget/subscriptionredemption/$', views.subscriptionredemption),
    url(r'^api/widget/fundgrossasset1/$', views.fundgrossasset1),
    url(r'^api/widget/fundgrossasset2/$', views.fundgrossasset2),
    url(r'^api/widget/fundgrossasset3/$', views.fundgrossasset3),
    url(r'^api/widget/fundgrossasset4/$', views.fundgrossasset4),
    url(r'^api/widget/fundsubredtable/$', views.fundsubredtable),
    url(r'^api/widget/currencyhedge/$', views.currencyhedge),
    #url(r'^api/widget/holdliquidity/$', views.holdliquidity),
    url(r'^api/widget/fundreturn/$', views.fundreturn),
    url(r'api/', include(widget.urls)),
    url(r'', include(api.urls)),
    url(r'admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^api/', include(v1_api.urls)),
    )

