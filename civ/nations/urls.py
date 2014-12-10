from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from nations import views
from django.views.generic.edit import CreateView

urlpatterns = patterns('',
    url(r'^$', views.indexView.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': '/'}, name='logout'),
    url(r'^register/$', views.registerView.as_view(), name='register'),
    url(r'^nation/(?P<pk>\d+)/$', views.nationView.as_view(), name='nation'),
    url(r'^edit_nation/(?P<pk>\d+)/$', views.editNationView.as_view(), name='edit_nation'),
    
)

urlpatterns += staticfiles_urlpatterns()
