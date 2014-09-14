__author__ = 'feiyicheng'

from django.shortcuts import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
import json


def login(request):
    para = request.REQUEST
    if 'username' in para.keys() and 'password' in para.keys():
        user = User.objects.get(username=para['username'])
        if user.check_password(para['password']):
            # return HttpResponse(user.username + 'heh')

            token = default_token_generator.make_token(user)
            data = {
                'status': 'success',
                'token': token,
                'user': user.username
            }
        else:
            data = {
                'status': 'error',
                'reason': 'password not correct'
            }
        return HttpResponse(json.dumps(data))

    return HttpResponse('hehe' + str(para))
