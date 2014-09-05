__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = ('',
    url(r'^oauth/authorize/$', ),
    url(r'^oauth/google/$', 'my_auth.google_oauth.login_start')

)



