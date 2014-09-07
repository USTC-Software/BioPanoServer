__author__ = 'feiyicheng'

import urllib2, urllib
import json
from urllib import urlencode, unquote
import re
import socket
from ssl import SSLError
import IGEMServer.settings as settings


class OAuthClientBase(object):
    def __init__(self):
        self.CLIENT_ID = ''
        self.CLIENT_SECRET = ''
        self.REDIRECT_URL = ''
        self.BASE_URL = ''
        self.TOKEN_METHOD = ''
        self.AUTHORIZATION_CODE_REQ = None

    def retrieve_tokens(self, para):
        authorization_token_req = {
            'code': para['code'],
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'redirect_uri': self.REDIRECT_URL,
            'grant_type': 'authorization_code',
        }

        cleanurl = self.BASE_URL + 'token'

        if self.TOKEN_METHOD == 'GET' or self.TOKEN_METHOD == '':
            url = cleanurl + '?' + urlencode(authorization_token_req)
            tokens_origin = urllib2.urlopen(url).read()
            access_token = re.match(r'access_token=(.+)&.*', tokens_origin).group(1)
            expires_in = re.match(r'in=(.+).*', tokens_origin).groups(1)
            self.USER_INFO_REQ['access_token'] = access_token
            return {'access_token': access_token, 'expires_in': expires_in}

        elif self.TOKEN_METHOD == 'POST':
            '''
            con = httplib.HTTPSConnection('accounts.google.com')
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Host': 'accounts.google.com',
            }
            con.request(method='POST', url='/o/oauth2/token', body=urlencode(authorization_token_req), headers=headers)
            response = con.getresponse()
            if response.status == 200:
                tokens_origin = response.read()
            con.close()
            '''
            data = urllib.urlencode(authorization_token_req)
            req = urllib2.Request(cleanurl, data)
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            # req.add_header('Host', 'accounts.google.com')
            response = urllib2.urlopen(req)
            tokens_origin = response.read()
            return json.loads(tokens_origin)
        else:
            pass


class OAuthClientGoogle(OAuthClientBase):
    def __init__(self):
        self.CLIENT_ID = settings.OAuthClient['google']['CLIENT_ID']
        self.CLIENT_SECRET = settings.OAuthClient['google']['CLIENT_SECRET']
        self.REDIRECT_URL = settings.OAuthClient['google']['REDIRECT_URL']
        self.BASE_URL = settings.OAuthClient['google']['BASE_URL']
        self.TOKEN_METHOD = 'POST'

        self.AUTHORIZATION_CODE_REQ = {
            'response_type': 'code',
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'scope': r'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
            'state': 'something'
        }

    # def retrieve_tokens(self, para):
    # tokens_origin = self._retrieve_tokens(para)
    #     # tokens_origin is json format
    #     tokens = json.loads(tokens_origin)
    #     return tokens
    def retrieve_tokens(self, para):
        authorization_token_req = {
            'code': para['code'],
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'redirect_uri': self.REDIRECT_URL,
            'grant_type': 'authorization_code',
        }

        cleanurl = self.BASE_URL + 'token'
        data = urllib.urlencode(authorization_token_req)
        req = urllib2.Request(cleanurl, data)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        # req.add_header('Host', 'accounts.google.com')
        tag = 1
        while 0 < tag < 5:
            try:
                response = urllib2.urlopen(req, timeout=4)
            except SSLError:
                tag += 1
                print('time out !')
                continue
            except Exception, e:
                tag += 1
                print('other errors' + e)
                continue
            else:
                break


        tokens_origin = response.read()
        return json.loads(tokens_origin)

    def get_info(self, access_token):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s' % (access_token,)
        # profile_json = urllib2.urlopen(url).read()
        tag = 1
        while 0 < tag < 5:
            try:
                response = urllib2.urlopen(url, timeout=4)
            except SSLError:
                tag += 1
                print('time out !')
                continue
            except Exception, e:
                tag += 1
                print('other errors' + e)
                continue
            else:
                if tag >= 5:
                    return None
                break


        profile = json.loads(response.read())
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

    # def retrieve_tokens(self, para):
    # tokens_origin = OAuthClientBase._retrieve_tokens(self, para)
    #     access_token = re.match(r'access_token=(.+)&.*', tokens_origin).group(1)
    #     expires_in = re.match(r'in=(.+).*', tokens_origin).groups(1)
    #     self.USER_INFO_REQ['access_token'] = access_token
    #     return {'access_token': access_token, 'expires_in': expires_in}

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


if __name__ == '__main__':
    pass




