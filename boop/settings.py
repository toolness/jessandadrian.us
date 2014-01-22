"""
Django settings for boop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import urlparse
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if sys.argv[:2] == ['manage.py', 'runserver']:
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
    os.environ['SECRET_KEY'] = 'development mode, yo'
    os.environ['DEBUG'] = ''
    # TODO: Support any alternative port passed-in from the command-line.
    os.environ['PORT'] = '8000'
    # TODO: Set ORIGIN to include any passed-in IP address.

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = TEMPLATE_DEBUG = 'DEBUG' in os.environ
PORT = int(os.environ['PORT'])

if DEBUG and not 'ORIGIN' in os.environ:
    os.environ['ORIGIN'] = 'http://localhost:%d' % PORT

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
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'boop.urls'

WSGI_APPLICATION = 'boop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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
