from django.conf.urls import patterns, url

from publishing import views

#print 'dir: ' + str(dir(views))
from publishing.views import FacetsView

urlpatterns = patterns('',
	#url(r'groups/(?P<username>\w+)$',views.groups,name='groups'),
	url(r'^facets/', FacetsView.as_view()),
	
	#url(r'^$', views.index, name='index'),
)
