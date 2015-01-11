from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^administration/', include(admin.site.urls)),
	url(r'^event/',include('events.urls')),
)
