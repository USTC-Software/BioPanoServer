__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^node/$', views.add_node),    # POST
    url(r"^node/(?P<id>[\w]+)/$", views.get_del_addref_node),  # DELETE / PUT / GET

    url(r'^link/$', views.add_link),    # POST
    url(r'^link/(?P<id>[\w]+)/$', views.get_del_addref_link),  # DELETE / PUT / GET


)