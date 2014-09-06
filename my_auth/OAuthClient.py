__author__ = 'feiyicheng'

import urllib2
import json
from urllib import urlencode, unquote
import re
import httplib


class OAuthClientBase(object):
    def __init__(self):
        self.CLIENT_ID = ''
        self.CLIENT_SECRET = ''
        self.REDIRECT_URL = ''
        self.BASE_URL = ''
        self.TOKEN_METHOD = ''
        self.AUTHORIZATION_CODE_REQ = None

    def _retrieve_tokens(self, para):
        authorization_token_req = {
            'code': para['code'],
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'redirect_uri': self.REDIRECT_URL,
            'grant_type': 'authorization_code',
        }

        cleanurl = self.BASE_URL + 'token/'

        if self.TOKEN_METHOD == 'GET' or self.TOKEN_METHOD == '':
            url = cleanurl + '?' + urlencode(authorization_token_req)
            tokens_origin = urllib2.urlopen(url).read()
        elif self.TOKEN_METHOD == 'POST':
            con = httplib.HTTPSConnection('accounts.google.com')
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Host': 'accounts.google.com',
            }
            con.request(method='POST', url='/o/oauth2/token', body=urlencode(authorization_token_req), headers=headers)
            response = con.getresponse()
            if response.status == 200:
                tokens_origin = response.read()
            con.close()

        return tokens_origin


class OAuthClientGoogle(OAuthClientBase):
    def __init__(self):
        self.CLIENT_ID = '803598705759-nuc4bd5cm9k0ng4u91m9fa3pr05158k9.apps.googleusercontent.com'
        self.CLIENT_SECRET = 'OlSa44n2HuYPfXyGPoCsXEeb'
        self.REDIRECT_URL = 'http://master.server.ailuropoda.org/auth/oauth/google/complete/'
        self.BASE_URL = r'https://accounts.google.com/o/oauth2/'
        self.TOKEN_METHOD = 'POST'

        self.AUTHORIZATION_CODE_REQ = {
            'response_type': 'code',
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'scope': r'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
            'state': 'something'
        }

    def retrieve_tokens(self, para):
        tokens_origin = OAuthClientBase._retrieve_tokens(self, para)
        # tokens_origin is json format
        try:
            tokens = json.loads(tokens_origin)
        except Exception:
            print('json loads failed')
            tokens = None
        return tokens

    def get_info(self, access_token):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % (access_token,)
        profile_json = urllib2.urlopen(url).read()
        profile = json.loads(profile_json)
        return profile


class OAuthClientQQ(OAuthClientBase):
    def __init__(self):
        self.CLIENT_ID = '1102463122'
        self.CLIENT_SECRET = '7jPGJC0GJ3rCW5Km'
        self.REDIRECT_URL = 'http://master.server.ailuropoda.org/auth/oauth/qq/complete/'
        self.BASE_URL = 'https://graph.qq.com/oauth2.0/'
        self.TOKEN_METHOD = 'GET'

        self.AUTHORIZATION_CODE_REQ = {
            'response_type': 'code',
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'state': 'something'
        }
        self.USER_INFO_REQ = {
            'access_token': '',
            'oauth_consumer_key': self.CLIENT_ID,
            'openid': '',
        }

    def get_info(self, para):
        tokens = self.retrieve_tokens(para)
        self.retrieve_useropenid(tokens)
        userinfo = self.get_user_info()
        self.__init__()
        return userinfo

    def retrieve_tokens(self, para):
        tokens_origin = OAuthClientBase._retrieve_tokens(self, para)
        access_token = re.match(r'access_token=(.+)&.*', tokens_origin).group(1)
        expires_in = re.match(r'in=(.+).*', tokens_origin).groups(1)
        self.USER_INFO_REQ['access_token'] = access_token
        return {'access_token': access_token, 'expires_in': expires_in}

    def retrieve_useropenid(self, tokens):
        url = self.BASE_URL + 'me/?access_token=' + tokens['access_token']
        openid_json = re.match(r'.*[(](.+)[)].*', urllib2.urlopen(url).read()).group(1)
        openid = json.loads(openid_json)
        self.USER_INFO_REQ['openid'] = openid['openid']
        return openid

    def get_user_info(self):
        url = 'https://graph.qq.com/user/get_user_info?' + urlencode(self.USER_INFO_REQ)
        userinfo_json = urllib2.urlopen(url)
        userinfo = json.loads(userinfo_json)
        return userinfo






