__author__ = 'feiyicheng'
from django.shortcuts import HttpResponse


def group_authenticated(func):
    '''
        a decorator that ensures the group
    '''

    def wrap(request, *args, **kwargs):
        if request.REQUEST['group'] not in [g.name for g in request.user.groups.all()]:
            return HttpResponse("{'status':'error', 'reason':'group incorrect'}")
        else:
            return func(request, *args, **kwargs)



    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap
