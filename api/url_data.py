__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<species>[\w]+)/node/$', views.add_node),    # POST
    url(r"^(?P<species>[\w]+)/node/(?P<id>[\w]+)/$", views.get_del_addref_node),  # DELETE / PUT / GET

    url(r'^(?P<species>[\w]+)/link/$', views.add_link),    # POST
    url(r'^(?P<species>[\w]+)/link/(?P<id>[\w]+)/$', views.get_del_addref_link),  # DELETE / PUT / GET


)
