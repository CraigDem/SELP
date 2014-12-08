from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from nations import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': '/'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^nation/(?P<nation_id>\d+)/$', views.nation, name='nation'),
    url(r'^nation/$', views.nation, name='nation'),
    
)

urlpatterns += staticfiles_urlpatterns()
