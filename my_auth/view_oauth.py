__author__ = 'feiyicheng'

from django.shortcuts import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from urllib import urlencode
from .OAuthClient import OAuthClientGoogle, OAuthClientQQ



# not standard(qq is standardized)
def login_start_google(request):
    oauthclientgoogle = OAuthClientGoogle()

    authorization_code_req = {
        'response_type': 'code',
        'client_id': oauthclientgoogle.CLIENT_ID,
        'redirect_uri': oauthclientgoogle.REDIRECT_URL,
        'scope': r'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
        'state': 'something'
    }

    URL = oauthclientgoogle.BASE_URL + "auth?%s" % urlencode(authorization_code_req)
    # return HttpResponse("{'url':'%s'}" % (URL,))
    return HttpResponsePermanentRedirect(URL)


# not standard(qq is standardized)
def login_complete_google(request):
    '''
        step 1: get tokens using the code google responsed
        step 2: get user profile using token
    '''
    oauthclientgoogle = OAuthClientGoogle()

    print('get code from google')
    # get tokens

    para = request.GET

    tokens = oauthclientgoogle.retrieve_tokens(para)
    print(str(tokens))
    access_token = tokens['access_token']

    profile = oauthclientgoogle.get_info(access_token)
    print(str(profile))

    # login the user
    # return HttpResponse('profile get\n' + str(profile))

    user, token = _get_user_and_token(profile)
    if user:
        data = {
            'status': 'success',
            'token': token,
            'user': user.pk,
        }
    else:
        data = {
            'status': 'error',
            'reason': 'cannot find and create user, pls contact us'
        }

    return HttpResponse(json.dumps(data))





def login_start_qq(request):
    oauthclientqq = OAuthClientQQ()
    authorization_url = oauthclientqq.BASE_URL.join('authorize/?')
    authorization_code_req = oauthclientqq.AUTHORIZATION_CODE_REQ
    authorization_url_with_paras = authorization_url.join(urlencode(authorization_code_req))
    # return HttpResponse("{'url':'%s'}" % (authorization_url_with_paras,))
    return HttpResponsePermanentRedirect(authorization_url_with_paras)


def login_complete_qq(request):
    oauthclientqq = OAuthClientQQ()
    para = request.GET
    print para
    userinfo = oauthclientqq.get_info(para)
    return (str(userinfo))


def _get_user_and_token(profile):
    '''
    :param profile: information get from Google with OAuth access_token
    :return: it will be a tuple of (user, token) if everything goes right, otherwise None
    '''

    user, created = User.objects.get_or_create(username=profile['email'])
    _update_user(user, profile)
    token = default_token_generator.make_token(user)
    return (user, token) if user else (None, None)


def _update_user(user, profile):
    '''
    update user info with the newest information get from OAuth
    :param user: (User object)the user whose profile needs to update
    :param profile: (dict)the source of new info
    :return: None
    '''
    try:
        user.first_name = profile['given_name']
        user.last_name = profile['family_name']
        user.email = profile['email']
    except AttributeError, e:
        raise e
    except KeyError, e:
        raise e
    return None



