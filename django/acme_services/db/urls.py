from django.conf.urls import patterns, url

from db import views

urlpatterns = patterns('',
	url(r'groups/(?P<username>\w+)$',views.groups,name='groups'),
	url(r'roles/(?P<username>\w+)$',views.roles,name='roles'),
	url(r'publish/(?P<username>\w+)$',views.publish,name='publish'),
)
