from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.home(), name='home'),
    url(r'^rsvp$', views.home(show_rsvp_form=True), name='rsvp'),
    url(r'^rsvp/yay$', views.home(show_rsvp_form=True,
                                  rsvp_result='yay'), name='rsvp_yay'),
    url(r'^rsvp/boo$', views.home(show_rsvp_form=True,
                                  rsvp_result='boo'), name='rsvp_boo'),
    url(r'^routes\.js$', views.routes, name='routes'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
)
