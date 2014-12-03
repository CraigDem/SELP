from django.conf.urls import patterns, url

from nations import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^nation/(?P<nation_id>\d+)/$', views.nation, name='nation'),
)
