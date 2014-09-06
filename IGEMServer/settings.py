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
    'biopano',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    # 'my_auth.middleware.CookieToTokenMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
    # 'social_auth.backends.google.GoogleOAuth2Backend',
    # 'my_auth.TokenBackend.TokenBackend'
    'django.contrib.auth.backends.ModelBackend',
)

GOOGLE_OAUTH2_CLIENT_ID = '803598705759-nuc4bd5cm9k0ng4u91m9fa3pr05158k9.apps.googleusercontent.com'  # os.environ['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = 'OlSa44n2HuYPfXyGPoCsXEeb'  # os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']
# GOOGLE_WHITE_LISTED_DOMAINS = ['ailuropoda.org']
SOCIAL_AUTH_USER_MODEL = 'auth.User'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
# SOCIAL_AUTH_EXTRA_DATA = False

SOCIAL_AUTH_PIPELINE = (
    # 'social.pipeline.social_auth.social_details',
    # 'social.pipeline.social_auth.social_uid',
    # 'social.pipeline.social_auth.auth_allowed',
    'social_auth.backends.pipeline.social.social_auth_user',
    # 'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'social_auth.backends.pipeline.misc.save_status_to_session',

)




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
