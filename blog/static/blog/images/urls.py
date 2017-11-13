from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
			url(r'^about/$', views.about, name='about'),
			url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':'/home/anna/Documents/django_py/blog/static'}),
			)
			
