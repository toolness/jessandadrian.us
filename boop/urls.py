from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'jess.views.home', name='home'),
    url(r'^login$', 'jess.views.login', name='login'),
    url(r'^logout$', 'jess.views.logout', name='logout'),
)
