from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^acme_services/db/',include('db.urls')),
    url(r'^acme_services/publishing/',include('publishing.urls')),
    # Examples:
    # url(r'^$', 'esgf_groups.views.home', name='home'),
    # url(r'^esgf_groups/', include('esgf_groups.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
