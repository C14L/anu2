# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)
import os
import pymysql

# Import namespaced settings for anuncios app.
from .settings_anuncios import ANUNCIOS
# Import private settings, not in GIT.
from .settings_private import *

pymysql.install_as_MySQLdb()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.path.exists('/islocal.txt')
PRODUCTION = not DEBUG
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1
ALLOWED_HOSTS = []
ROOT_URLCONF = 'anu2.urls'
WSGI_APPLICATION = 'anu2.wsgi.application'
LANGUAGES = (('es', 'Espanol'), ('de', 'Deutsch'), ('en', 'English'))
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static_collected/')
if not PRODUCTION:
    # The Angular app is here. On the live system, the app is served by
    # nginx directly, same as the other static files.
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "ng-app"), )
MEDIA_URL = '/p/'
MEDIA_ROOT = 'media'
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dtrcity',
    'anuncios',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',  # {{MEDIA_URL}}
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


###############################################################################


# REST framework settings
# See http://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGINATE_BY': 100,
}
