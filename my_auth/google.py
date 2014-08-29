__author__ = 'feiyicheng'

from social_auth.backends.google import BaseOAuth2, GoogleOAuth2Backend, GOOGLE_OAUTH2_SCOPE, googleapis_profile
from social_auth.backends.google import GOOGLEAPIS_PROFILE, GoogleOAuth2


class MyGoogleOAuth2(BaseOAuth2):
    """Google OAuth2 support"""
    AUTH_BACKEND = GoogleOAuth2Backend
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
    ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    REVOKE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/revoke'
    REVOKE_TOKEN_METHOD = 'GET'
    SETTINGS_SECRET_NAME = 'GOOGLE_OAUTH2_CLIENT_SECRET'
    SCOPE_VAR_NAME = 'GOOGLE_OAUTH_EXTRA_SCOPE'
    DEFAULT_SCOPE = GOOGLE_OAUTH2_SCOPE
    REDIRECT_STATE = False

    print DEFAULT_SCOPE  #<------ to be sure

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        return googleapis_profile(GOOGLEAPIS_PROFILE, access_token)

    @classmethod
    def revoke_token_params(cls, token, uid):
        return {'token': token}

    @classmethod
    def revoke_token_headers(cls, token, uid):
        return {'Content-type': 'application/json'}


class SimplerGoogleOAuth2(GoogleOAuth2):
    DEFAULT_SCOPE = ['https://www.googleapis.com/auth/userinfo.email']
