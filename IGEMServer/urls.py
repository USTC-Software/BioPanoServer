from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IGEMServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include('api.url_data')),
    url(r'^search/', include('api.url_search')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}, name='static'),
    # url(r'^login/', 'my_auth.views.login_view'),    # POST
    # url(r'^logout/', 'my_auth.views.logout_view'),  # POST
    url(r'^auth/', include('my_auth.url_auth')),
    # url(r'^google-login', 'my_auth.views.google_login'),
    url(r'^/?$', 'IGEMServer.views.index'),
    url(r'^data/', include('biopano.urls')),
)
