from django.conf.urls import patterns, include, url
from django.contrib import admin

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
    url(r'^$', views.index, name='index'),
    url(r'^check-nodes/$', views.check_nodes),
    url(r'^mainmenu/$', views.mainmenu),
    url(r'api/', include(widget.urls)),
    url(r'', include(api.urls)),
    url(r'admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^api/', include(v1_api.urls)),
)

