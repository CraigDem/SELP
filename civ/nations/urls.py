from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from nations import views

urlpatterns = patterns('',
    url(r'^$', views.indexView.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': '/'}, name='logout'),
    url(r'^register/$', views.registerView.as_view(), name='register'),
    url(r'^nation/(?P<pk>\d+)/$', views.nationView.as_view(), name='nation'),
    url(r'^edit/(?P<pk>\d+)/$', views.editNationView.as_view(), name='editNation'),
    url(r'^expand/(?P<pk>\d+)/$', views.expandNationView.as_view(), name='expandNnation'),
    url(r'^bills/(?P<pk>\d+)/$', views.billsNationView.as_view(), name='payBills'),
    url(r'^taxes/(?P<pk>\d+)/$', views.taxesNationView.as_view(), name='collectTaxes'),
    url(r'^noEntry/$', views.noEntry.as_view(), name='noEntry'),
    url(r'^rank/$', views.rankNationView.as_view(), name='rank'),
)

urlpatterns += staticfiles_urlpatterns()
