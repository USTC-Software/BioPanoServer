__author__ = 'feiyicheng'

__author__ = 'feiyicheng'

from django.conf.urls import patterns, include, url
import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^search/$', 'projects.views.search'), # search project by author or name

    url(r'^create/(?P<prj_name>[^/]+)/$', 'projects.views.create_project'),  # create a new project
    # url(r'^addin/(?P<prj_id>[^/]+)$', 'projects.views.add_in_a_project'), # add the user into a project
    url(r'^delete/(?P<prj_id>\d+)/$', 'projects.views.delete_project'), # delete a project
    url(r'^addcollaborator/(?P<prj_id>[^/]+)/(?P<username>[^/]+)/$', 'projects.views.add_collaborator'),

    url(r'^my/$', 'projects.views.get_my_projects'),
    # url(r'^switch/(?P<prj_id>[^/]+)/$', 'projects.views.switch_project'),
)