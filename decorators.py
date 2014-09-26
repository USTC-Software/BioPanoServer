__author__ = 'feiyicheng'

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import HttpResponse
from django.http import QueryDict
from projects.models import Project
from django.core.exceptions import ObjectDoesNotExist


def logged_in(func):
    """
    :param func: a view methd . func(request,*args,**kwargs)
    :param args:
    :param kwargs:
    :return: func or response with error reason
    """

    def wrap(request, *args, **kwargs):
        try:
            if isinstance(request.user, AnonymousUser):
                # user not logged in
                return HttpResponse("{'status':'error','reason':'this operation need the user to be logged in'}")
            elif isinstance(request.user, User):
                # user already logged in
                return func(request, *args, **kwargs)
            else:
                raise TypeError('user type should be either User or AnonymousUser')
        except AttributeError:
            raise AttributeError('request does not has attribute user')


    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__

    return wrap


def project_verified(func):
    """

    :param func:
    :return:
    """

    def wrap(request, *args, **kwargs):
        data = QueryDict(request.body)
        if 'pid' not in data.keys():
            return func(request, *args, **kwargs)
        else:
            try:
                prj = Project.objects.get(pk=data['pid'])
            except ObjectDoesNotExist:
                return HttpResponse("{'status':'error', 'reason':'cannot find a project matching given pid'}")
            else:
                if request.user == prj.author or request.user in prj.collaborators:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponse("{'status':'error', 'reason':'the project cannot match the user logged in'}")

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__

    return wrap


def logged_in_exclude_get(func):
    """
    :param func: a view methd . func(request,*args,**kwargs)
    :param args:
    :param kwargs:
    :return: func or response with error reason
    """

    def wrap(request, *args, **kwargs):
        try:
            if isinstance(request.user, AnonymousUser):
                # user not logged in
                if request.method == 'GET':
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponse("{'status':'error','reason':'this operation need the user to be logged in'}")
            elif isinstance(request.user, User):
                # user already logged in
                return func(request, *args, **kwargs)
            else:
                raise TypeError('user type should be either User or AnonymousUser')
        except AttributeError:
            raise AttributeError('request does not has attribute user')


    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__

    return wrap


def project_verified_exclude_get(func):
    """

    :param func:
    :return:
    """

    def wrap(request, *args, **kwargs):
        if request.method == 'GET':
            return func(request, *args, **kwargs)
        data = QueryDict(request.body)
        if 'pid' not in data.keys():
            return func(request, *args, **kwargs)
        else:
            try:
                prj = Project.objects.get(pk=data['pid'])
            except ObjectDoesNotExist:
                return HttpResponse("{'status':'error', 'reason':'cannot find a project matching given pid'}")
            else:
                if request.user == prj.author or request.user in prj.collaborators:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponse("{'status':'error', 'reason':'the project cannot match the user logged in'}")

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__

    return wrap
