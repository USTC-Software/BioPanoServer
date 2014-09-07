__author__ = 'feiyicheng'

from django.shortcuts import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from urllib import urlencode
from .OAuthClient import OAuthClientGoogle, OAuthClientQQ

oauthclientqq = OAuthClientQQ()
oauthclientgoogle = OAuthClientGoogle()


# not standard(qq is standardized)
def login_start_google(request):
    authorization_code_req = {
        'response_type': 'code',
        'client_id': oauthclientgoogle.CLIENT_ID,
        'redirect_uri': oauthclientgoogle.REDIRECT_URL,
        'scope': r'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
        'state': 'something'
    }

    URL = oauthclientgoogle.BASE_URL + "auth?%s" % urlencode(authorization_code_req)
    # print URL
    return HttpResponse("{'url':'%s'}" % (URL,))


# not standard(qq is standardized)
def login_complete_google(request):
    '''
        step 1: get tokens using the code google responsed
        step 2: get user profile using token
    '''

    print('get code from google')
    # get tokens

    para = request.GET

    tokens = oauthclientgoogle.retrieve_tokens(para)
    # print(str(tokens))
    access_token = tokens['access_token']

    profile = oauthclientgoogle.get_info(access_token)
    # print(str(profile))

    # login the user

    try:
        user = User.objects.get(email=profile['email'])
    except MultipleObjectsReturned:
        return HttpResponse("{'status':'error', 'reason':'there are more than one user using this email'}")
    except ObjectDoesNotExist:
        # first login of the user
        User.objects.create_user(username=profile['email'], password=None, email=profile['email'])
        user = User.objects.get(username=profile['email'])
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        # user.save()
        if user:
            login(request, user)
        else:
            return HttpResponse("{'error':'cannot create user'}")

    else:
        # user exists
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        # user.save()
        login(request, user)

    return HttpResponse("{'status':'success'}")


def login_start_qq(request):
    global oauthclientqq
    authorization_url = oauthclientqq.BASE_URL.join('authorize/?')
    authorization_code_req = oauthclientqq.AUTHORIZATION_CODE_REQ
    authorization_url_with_paras = authorization_url.join(urlencode(authorization_code_req))
    return HttpResponse("{'url':'%s'}" % (authorization_url_with_paras,))


def login_complete_qq(request):
    global oauthclientqq
    para = request.GET
    userinfo = oauthclientqq.get_info(para)
