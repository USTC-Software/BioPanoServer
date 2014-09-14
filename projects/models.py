__author__ = 'feiyicheng'

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    '''
    a class that represents a project in which user can cooperate together

    '''
    author = models.OneToOneField(User, related_name='author')
    collaborators = models.ManyToManyField(User, blank=True, related_name='collaborators')
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=300, blank=True, default="no description yet")

