from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^rsvp$', views.rsvp, name='rsvp'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
)
