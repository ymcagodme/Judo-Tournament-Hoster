from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'members.views.index'),
    url(r'^query_all$', 'members.views.query_all'),
    url(r'^query_dojo$', 'members.views.query_dojo'),
    url(r'^query_top5$', 'members.views.query_top5'),
    url(r'^query_completed$', 'members.views.query_completed'),
    url(r'^admin/', include(admin.site.urls)),
)
