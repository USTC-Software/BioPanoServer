__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views

urlpatterns = ('',
    url(r'^oauth/authorize/$', 'my_auth.views.')

)



