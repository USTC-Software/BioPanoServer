__author__ = 'feiyicheng'

from rest_framework.authtoken.models import Token
from django.shortcuts import HttpResponse
from rest_framework import HTTP_HEADER_ENCODING, exceptions


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header

    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if type(auth) == type(''):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenMiddleware(object):
    model = Token

    def process_request(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        key = auth[1]
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            return HttpResponse("{'status':'error', 'reason':'invalid token'}")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        request.user = token.user
        return None



