from django.conf.urls import patterns, url

from publishing import views

urlpatterns = patterns('',
	url(r'base_facets/(?P<username>\w+)$',views.base_facets,name='base_facets'),
)
