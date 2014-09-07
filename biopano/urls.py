from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IGEMServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^node/(?P<obj_id>[\w]+)/link/$', views.look_around),    # POST
    url(r'^')

)
