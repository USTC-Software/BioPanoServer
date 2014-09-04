__author__ = 'feiyicheng'

from django.shortcuts import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import urllib2
import httplib
import json
from urllib import urlencode

'''
global variables
'''
CLIENT_ID = '803598705759-nuc4bd5cm9k0ng4u91m9fa3pr05158k9.apps.googleusercontent.com'
CLIENT_SECRET = 'OlSa44n2HuYPfXyGPoCsXEeb'
REDIRECT_URL = 'http://master.server.ailuropoda.org/auth/complete/'
BASE_URL = r"https://accounts.google.com/o/oauth2/"
AUTHORIZATION_CODE = ''
ACCESS_TOKEN = ''


def login_start(request):

    authorization_code_req = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URL,
        'scope': r'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
        'state': 'something'
    }

    URL = BASE_URL + "auth?%s" % urlencode(authorization_code_req)
    # print URL
    return HttpResponsePermanentRedirect(URL)


def login_complete(request):
    '''
        step 1: get tokens using the code google responsed
        step 2: get user profile using token
    '''

    print('get code from google')
    # get tokens

    para = request.GET
    authorization_token_req = {
        'code': para['code'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URL,
        'grant_type': 'authorization_code',
    }

    url = BASE_URL + 'token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Host': 'accounts.google.com',
               }

    dataencoded = urlencode(authorization_token_req)
    print(url + ' ' + urlencode(authorization_token_req))

    con = httplib.HTTPSConnection('accounts.google.com')
    con.request(method='POST', url='/o/oauth2/token', body=dataencoded, headers=headers)
    response = con.getresponse()
    if response.status == 200:
        print('success')
        tokens_json = response.read()
        print(str(type(tokens_json)) + '\n' + tokens_json)
    con.close()

    # get access_token
    try:
        tokens = json.loads(tokens_json)
    except:
        print('json loads failed')
        tokens = None

    try:
        access_token = tokens['access_token']
    except KeyError:
        print('no such key:access_token')
        access_token = None


    # get profile

    url = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % (access_token,)
    profile_json = urllib2.urlopen(url).read()
    profile = json.loads(profile_json)


    #login the user
    try:
        user = User.objects.get(email=profile['email'])
    except MultipleObjectsReturned:
        return HttpResponse("{'status':'error', 'reason':'there are more than one user using this email'}")
    except ObjectDoesNotExist:
        # first login of the user
        print('first login')
        User.objects.create_user(username=profile['email'], password=None, email=profile['email'])
        user = User.objects.get(email=profile['email'])
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        print('new user created!')
        login(request=request, user=user)
        print('user login successfully')
    else:
        # the user already exists

        # update user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        print('welcome back')
        print(str(user.is_authenticated()))
        user.save()
        login(request, user)
        print('user login successfully')

    return HttpResponse("{'status':'success'}")
