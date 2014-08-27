__author__ = 'feiyicheng'

from django.conf.urls import *
from django.contrib import admin
from .views import AuthComplete, LoginError


admin.autodiscover()

urlpatterns = patterns('',
    # some other urls
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
    url(r'', include('social_auth.urls')),
)