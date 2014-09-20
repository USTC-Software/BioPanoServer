__author__ = 'feiyicheng'
from django.shortcuts import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict

def group_authenticated(func):
    """
        a decorator that ensures the group
    """

    def wrap(request, *args, **kwargs):
        if request.REQUEST['group'] not in [g.name for g in request.user.groups.all()]:
            return HttpResponse("{'status':'error', 'reason':'group incorrect'}")
        else:
            return func(request, *args, **kwargs)


    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap


def user_verified(func):
    """
    a decorator that authenticate the user using tokens
    if authenticated successfully, the specific user object will be in request.user
    """

    def wrap(request, *args, **kwargs):
        if request.method == 'GET' or 'POST':
            para = request.REQUEST
        elif request.method == 'PUT':
            para = QueryDict(request.body)
            request.PUT = para
        elif request.method == 'PATCH':
            para = QueryDict(request.body)
            request.PATCH = para
        elif request.method == 'DELETE':
            para = QueryDict(request.body)
            request.DELETE = para

        # GET method does not need the user to be logged in
        if request.method == 'GET':
            return func(request, *args, **kwargs)

        if ('token' not in para.keys()) or ('username' not in para.keys()):
            return HttpResponse("{'status':'error', 'reason':'your request paras should include username & token '}")
        else:
            try:
                user = User.objects.get(username=para['username'])
            except ObjectDoesNotExist:
                return HttpResponse("{'status':'error', 'reason':'the username is incorrect'}")
            else:
                # find the user with given username
                valid = default_token_generator.check_token(user=user, token=para['token'])
                if valid:
                    request.user = user
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponse("{'status':'error', 'reason':'token incorrect or expired ,pls ask for token again'}")

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap

