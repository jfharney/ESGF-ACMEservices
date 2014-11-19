from django.conf.urls import patterns, url

from groups import views

urlpatterns = patterns('',
	url(r'(?P<username>\w+)$',views.groups,name='groups'),
)
