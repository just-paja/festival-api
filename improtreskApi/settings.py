"""
Django settings for improtreskApi project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import datetime

import os

from django_auth_ldap.config import GroupOfNamesType, LDAPSearch

import ldap

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.realpath(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    ')zbzb++_y*p)2m*cqm)yz^@2sl^sa+%8$dwl$iex7=ai$42cw$',
)

AUTHENTICATION_BACKENDS = (
    'api.auth.participant_backend.ParticipantBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AWS_ACCESS_KEY_ID = os.environ.get('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('DJANGO_AWS_STORAGE_BUCKET_NAME')

DEBUG = os.environ.get('DJANGO_DEBUG', True)

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'django_extensions',
    'storages',
    'dbbackup',
    'mathfilters',
    'api',
    'api_textual',
    'api_admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'improtreskApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'improtreskApi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DJANGO_DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('DJANGO_DB_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DB_HOST', ''),
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'cs-cz'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

EMAIL_SENDER = 'info@improtresk.cz'
EMAIL_TECH = 'tech@improliga.cz'

YEAR = 2017
RESERVATION_DURATION_SHORT = datetime.timedelta(hours=2)
RESERVATION_DURATION_PAYMENT = datetime.timedelta(days=5)

FIO_TOKEN = os.environ.get('DJANGO_FIO_TOKEN', '')

AUTH_LDAP_SERVER_URI = os.environ.get('DJANGO_LDAP_SERVERI_URI', '')
AUTH_LDAP_BIND_DN = os.environ.get('DJANGO_LDAP_BIND_DN', '')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('DJANGO_LDAP_BIND_PASSWORD', '')
AUTH_LDAP_USER_SEARCH_BASE = os.environ.get('DJANGO_LDAP_USER_SEARCH_BASE', '')
AUTH_LDAP_USER_SEARCH_FORMAT = os.environ.get('DJANGO_LDAP_USER_SEARCH_FORMAT', '')
AUTH_LDAP_GROUP_SUPERUSER = os.environ.get('DJANGO_LDAP_GROUP_SUPERUSER', '')
AUTH_LDAP_GROUP_STAFF = os.environ.get('DJANGO_LDAP_GROUP_STAFF', '')

AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_USER_ATTR_MAP = {"email": "mail"}

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

try:
    from local_settings import *  # noqa
except ImportError:
    pass

if AUTH_LDAP_SERVER_URI:
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        AUTH_LDAP_USER_SEARCH_BASE,
        ldap.SCOPE_SUBTREE,
        AUTH_LDAP_USER_SEARCH_FORMAT,
    )

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        AUTH_LDAP_USER_SEARCH_BASE,
        ldap.SCOPE_SUBTREE,
        "(objectClass=groupOfNames)",
    )

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_superuser": AUTH_LDAP_GROUP_SUPERUSER,
        "is_staff": AUTH_LDAP_GROUP_STAFF,
    }

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
    ) + AUTHENTICATION_BACKENDS

if AWS_ACCESS_KEY_ID:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DBBACKUP_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DBBACKUP_STORAGE_OPTIONS = {
        'access_key': AWS_ACCESS_KEY_ID,
        'secret_key': AWS_SECRET_ACCESS_KEY,
        'bucket_name': AWS_STORAGE_BUCKET_NAME,
    }

if DEBUG:
    MEDIA_ROOT = '/var/tmp/improtresk-api'
    MEDIA_URL = '/media/'
else:
    X_FRAME_OPTIONS = 'DENY'
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
