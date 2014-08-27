__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^node/$', views.add_node),    # POST
    url(r"^node/(?P<id>[^/]+)/$", views.del_or_addref_node),  # DELETE / PUT
    url(r'^node/search/$', views.search_json_node),    # POST
    url(r'^link/$', views.add_link),    # POST
    url(r'^link/(?P<id>[^/]+)/$', views.del_or_addref_link),  # DELETE / PUT
    url(r'^link/search/$', views.search_json_link),  # POST
)
