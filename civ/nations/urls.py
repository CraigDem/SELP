from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from nations import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^nation/(?P<nation_id>\d+)/$', views.nation, name='nation'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)

urlpatterns += staticfiles_urlpatterns()
