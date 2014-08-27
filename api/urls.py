__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^node/$', views.add_node),    # POST
    url(r"^node/(?P<id>[^/]+)/$", views.delete_node),  # DELETE
    url(r'^node/search/$', views.search_json_node),    # POST
    url(r'^node/$', views.addref_node),    # PUT
    url(r'^link/add/$', views.add_link),    # POST
    url(r'^link/delete/$', views.delete_link),  # DELETE
    url(r'^link/search/$', views.search_json_link),  # POST
    url(r'^link/add_ref/$', views.addref_link),  # PUT
)
