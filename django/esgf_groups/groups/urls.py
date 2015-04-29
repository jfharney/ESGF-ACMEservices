from django.conf.urls import patterns, url

from groups import views

urlpatterns = patterns('',
	url(r'groups/(?P<username>\w+)$',views.groups,name='groups'),
	url(r'roles/(?P<username>\w+)$',views.roles,name='roles'),
	url(r'publish/(?P<username>\w+)$',views.publish,name='publish'),
	url(r'base_facets/(?P<username>\w+)$',views.base_facets,name='base_facets'),
)
