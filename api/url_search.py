__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<species>[\w]+)/node/$', views.search_json_node),    # POST
    url(r'^(?P<species>[\w]+)/link/$', views.search_json_link),  # POST
)

