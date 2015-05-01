from django.conf.urls import patterns, url

from publishing import views

urlpatterns = patterns('',
	url(r'base_facets/(?P<username>\w+)$',views.base_facets,name='base_facets'),
	url(r'publish_data/(?P<username>\w+)$',views.publish_data,name='publish_data'),
)
