__author__ = 'feiyicheng'

from django.db import models
from mongoengine.document import Document
import mongoengine.fields as fields
# from django.contrib.auth.models import User
from mongoengine.django.auth import User


class Project(models.Model):
    """
    a class that represents a project in which user can cooperate together

    """
    author = models.ForeignKey(User, related_name='projects_authored')
    collaborators = models.ManyToManyField(User, blank=True, related_name='projects_collaborated')
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=300, blank=True, default="no description yet")
    species = models.TextField(max_length=100, blank=True)
    is_active = models.BooleanField()  # this field will be set False if it is 'deleted' ,to keep prj_id
                                        # still all the time

    def __unicode__(self):
        return "name:" + self.name + " author:" + self.author


class ProjectMongo(Document):
    """
    a class that represents a project in which user can cooperate together

    """
    author = fields.ReferenceField(User, required=True)
    collaborators = fields.ListField(field=User)
    name = fields.StringField(max_length=40)
    description = fields.StringField(max_length=1000)
    species = fields.StringField(max_length=100)
    is_active = fields.BooleanField(default=True)


class UserProfile(models.Model):
    """
    Profile of user that stores extra info of User
    """
    user = models.OneToOneField(User, related_name='userprofile')
    currentProject = models.ForeignKey(Project, blank=True, related_name='+')  # just store the info of the latest prj











