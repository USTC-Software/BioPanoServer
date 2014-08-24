__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^node/add/$', views.add_node),
    url(r'^node/delete/$', views.delete_node),
    url(r'^node/search/$', views.search_json_node),
    url(r'^node/add/$', views.add_link),
    url(r'^node/delete/$', views.delete_link),
    url(r'^node/search/$', views.search_json_link),
)
