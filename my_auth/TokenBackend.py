__author__ = 'feiyicheng'

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator


class TokenBackend(ModelBackend):
    def authenticate(self, email, token=None):
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return None

        if default_token_generator.check_token(user, token):
            return user
        return None
