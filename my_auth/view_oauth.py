__author__ = 'feiyicheng'

from django.shortcuts import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from urllib import urlencode
from OAuthClient import OAuthClientGoogle, OAuthClientQQ
from socialoauth import SocialSites, SocialAPIError
from settings import SOCIALOAUTH_SITES


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

    (user, token) = _get_user_and_token(profile)
    if user:
        data = {
            'status': 'success',
            'token': str(token),
            'user': user.pk,
        }
    else:
        data = {
            'status': 'error',
            'reason': 'cannot find or create user, pls contact us',
        }

    return HttpResponse(json.dumps(data))


def login_start_qq(request):
    oauthclientqq = OAuthClientQQ()
    authorization_url = oauthclientqq.BASE_URL + 'authorize/?'
    authorization_code_req = oauthclientqq.AUTHORIZATION_CODE_REQ
    authorization_url_with_paras = authorization_url + urlencode(authorization_code_req)
    # return HttpResponse("{'url':'%s'}" % (authorization_url_with_paras,))
    return HttpResponsePermanentRedirect(authorization_url_with_paras)


def login_complete_qq(request):
    oauthclientqq = OAuthClientQQ()
    para = request.GET
    print para
    userinfo = oauthclientqq.get_info(para)
    return (str(userinfo))


def login_start_baidu(request):
    #site = SocialSites(SOCIALOAUTH_SITES).get_site_object_by_name('baidu')
    #authorize_url = site.authorize_url
    socialsites = SocialSites(SOCIALOAUTH_SITES)
    for s in socialsites.list_sites_class():
        site = socialsites.get_site_object_by_class(s)
        authorize_url = site.authorize_url
    return HttpResponsePermanentRedirect(authorize_url)


def login_complete_baidu(request):
    code = request.GET.get('code')
    if not code:
        data = {
            'status': 'error',
            'reason': 'cannot find or create user, pls contact us',
        }
        return HttpResponse(json.dumps(data))
    site = SocialSites(SOCIALOAUTH_SITES).get_site_object_by_name('baidu')
    try:
        site.get_access_token(code)
    except SocialAPIError as e:
        data = {
            'status': 'error',
            'reason': e.error_msg,
        }
        return HttpResponse(json.dumps(data))
    profile = {}
    profile['uid'] = site.uid
    profile['given_name'] = site.name
    profile['family_name'] = ''
    profile['email'] = ''
    (user, token) = _get_user_and_token(profile)
    if user:
        data = {
            'status': 'success',
            'token': str(token),
            'user': user.pk,
        }
    else:
        data = {
            'status': 'error',
            'reason': 'cannot find or create user, pls contact us',
        }
    return HttpResponse(json.dumps(data))


def _get_user_and_token(profile):
    """
    :param profile: information get from Google with OAuth access_token
    :return: it will be a tuple of (user, token) if everything goes right, otherwise None
    """

    user, created = User.objects.get_or_create(username=profile['uid'])
    _update_user(user, profile)
    token, created = Token.objects.get_or_create(user=user)
    return (user, token) if user else (None, None)


def _update_user(user, profile):
    """
    update user info with the newest information get from OAuth
    :param user: (User object)the user whose profile needs to update
    :param profile: (dict)the source of new info
    :return: None
    """
    try:
        user.first_name = profile['given_name']
        user.last_name = profile['family_name']
        user.email = profile['email']
    except AttributeError, e:
        raise e
    except KeyError, e:
        raise e
    return None




