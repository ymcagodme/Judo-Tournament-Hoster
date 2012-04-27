from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'members.views.index'),
    url(r'^query_all$', 'members.views.query_all'),
    url(r'^query_dojo$', 'members.views.query_dojo'),
    url(r'^query_top5$', 'members.views.query_top5'),
    url(r'^query_completed$', 'members.views.query_completed'),
    url(r'^members/(?P<pk>\d+)/$', 'members.views.query_member'),
    url(r'^members/(?P<pk>\d+)/check_in$', 'members.views.check_in_member'),
    url(r'^members/(?P<pk>\d+)/weight_in$', 'members.views.weight_in_member'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {}),

    url(r'^admin/gen_dojo_result$', 'members.admin_views.gen_dojo_result'),
    url(r'^admin/echo$', 'members.admin_views.echo'),
    url(r'^admin/members/match/add_multiple/$', 'members.admin_views.add_multiple_matches'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)
