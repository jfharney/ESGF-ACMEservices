from django.conf.urls import patterns, url

from db import views

#print 'dir: ' + str(dir(views))
from db.views import GroupView

urlpatterns = patterns('',
	#url(r'groups/(?P<username>\w+)$',views.groups,name='groups'),
	url(r'^groups/(?P<username>\w+)$', GroupView.as_view()),
	
	#url(r'^$', views.index, name='index'),
)
