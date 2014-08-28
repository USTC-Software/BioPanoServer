"""
Django settings for IGEMServer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7jkomavmtmlifw$pbs9@wu%y^=sn37xv0on+z9@0oqp0_g7ilu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'IGEMServer',
    'social_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

'''
following are:
    AUTH CONFIG------GOOGLE & LDAP
'''

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/auth/logged-in/'
LOGIN_ERROR_URL = '/auth/login-error/'

GOOGLE_OAUTH2_CLIENT_ID = '803598705759-nuc4bd5cm9k0ng4u91m9fa3pr05158k9.apps.googleusercontent.com'  # os.environ['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = 'OlSa44n2HuYPfXyGPoCsXEeb'  # os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']
# GOOGLE_WHITE_LISTED_DOMAINS = ['ailuropoda.org']
SOCIAL_AUTH_USER_MODEL = 'auth.User'

TEMPLATE_CONTEXT_PROCESSORS = (
    "social_auth.context_processors.social_auth_by_type_backends",
)



# LDAP configure
AUTH_LDAP_SERVER_URI = "ldap://ldap.ailuropoda.org"
import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType, GroupOfNamesType, ActiveDirectoryGroupType

AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
AUTH_LDAP_BIND_DN = "cn=admin,dc=ailuropoda,dc=org"
AUTH_LDAP_BIND_PASSWORD = "SyntheticBiology"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,dc=ailuropoda,dc=org",
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 0,
    ldap.OPT_REFERRALS: 0,
}
# mapping

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_MIRROR_GROUPS = True
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,dc=ailuropoda,dc=org", ldap.SCOPE_SUBTREE, "(objectClass=top)")

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active,ou=groups,dc=ailuropoda,dc=org",
    "is_staff": "cn=staff,ou=groups,dc=ailuropoda,dc=org",
    "is_superuser": "cn=superuser,ou=groups,dc=ailuropoda,dc=org",
}

import logging

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
# end ldap log

ROOT_URLCONF = 'IGEMServer.urls'

WSGI_APPLICATION = 'IGEMServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'backend_master',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'master',
        'PASSWORD': 'SyntheticBiology',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',  # Set to empty string for default.
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)