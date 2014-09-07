__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^oauth/authorize/$', ),
    url(r'^oauth/google/login/$', 'my_auth.view_oauth.login_start_google'),
    url(r'^oauth/google/complete/$', 'my_auth.view_oauth.login_complete_google'),
    url(r'^oauth/qq/login/$', 'my_auth.view_oauth.login_start_qq'),
    url(r'^oauth/qq/complete/', 'my_auth.view_oauth.login_complete_qq'),
    # url(r'^token/new/$', 'my_auth.view_token.token_new'),
)



