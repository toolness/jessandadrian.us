from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^rsvp$', views.rsvp, name='rsvp'),
    url(r'^rsvp/yay$', views.rsvp_yay, name='rsvp_yay'),
    url(r'^rsvp/boo$', views.rsvp_boo, name='rsvp_boo'),
    url(r'^routes\.js$', views.routes, name='routes'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
)
