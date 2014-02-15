"""
Django settings for website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import urlparse
import dj_database_url

from .settings_utils import set_default_env, set_default_db, \
                            parse_email_backend_url, \
                            parse_secure_proxy_ssl_header

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
path = lambda *parts: os.path.join(BASE_DIR, *parts)

if os.path.basename(sys.argv[0]) == 'manage.py':
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
    set_default_env(
        SECRET_KEY='development mode',
        DEBUG='indeed',
        # TODO: Support any alternative port passed-in from the command-line.
        PORT='8000',
        # TODO: Set ORIGIN to include any passed-in IP address.
        EMAIL_BACKEND_URL='console:',
    )

if 'SECURE_PROXY_SSL_HEADER' in os.environ:
    SECURE_PROXY_SSL_HEADER = parse_secure_proxy_ssl_header(
        os.environ['SECURE_PROXY_SSL_HEADER']
    )

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = TEMPLATE_DEBUG = 'DEBUG' in os.environ
PORT = int(os.environ['PORT'])

if DEBUG: set_default_env(ORIGIN='http://localhost:%d' % PORT)

set_default_db('sqlite:///%s' % path('db.sqlite3'))

globals().update(parse_email_backend_url(os.environ['EMAIL_BACKEND_URL']))

ORIGIN = os.environ['ORIGIN']

ALLOWED_HOSTS = [urlparse.urlparse(ORIGIN).hostname]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'jess'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

import os

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    
)
