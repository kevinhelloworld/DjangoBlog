"""blog的url模式"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 
		views.AchivesView.as_view(), name='achives'),
	url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
	url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),	
	#搜索信息
	url(r'^search/$', views.search, name='search'),
	url(r'^about/$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
]
