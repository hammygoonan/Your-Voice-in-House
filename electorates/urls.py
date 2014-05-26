from django.conf.urls import patterns, url

from electorates import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)