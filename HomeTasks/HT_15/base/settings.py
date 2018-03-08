"""
Django settings for base project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
import subprocess

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "b+t4rgjh%7b#)y7_(py6p8okuo+2z@73leywg_c7f*-4a7e=j3"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'hn_parser',
    'stories',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

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

                'stories.context_processors.context_processors.categories',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
# Uncomment if use Postgres
# DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


_m_loc = os.environ.get('MEMCACHEDCLOUD_SERVERS')
_m_user = os.environ.get('MEMCACHEDCLOUD_USERNAME')
_m_pwd = os.environ.get('MEMCACHEDCLOUD_PASSWORD')
if _m_loc is None:
    command = 'heroku config:get MEMCACHEDCLOUD_SERVERS'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    _m_loc, error = process.communicate()

    command = 'heroku config:get MEMCACHEDCLOUD_USERNAME'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    _m_user, error = process.communicate()

    command = 'heroku config:get MEMCACHEDCLOUD_PASSWORD'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    _m_pwd, error = process.communicate()

    def decode_and_strip(a):
        return a.decode().strip()

    (_m_loc, _m_user, _m_pwd) = map(lambda x: x.decode().strip(), (_m_loc, _m_user, _m_pwd))

_m_loc = _m_loc.split(',')
CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': _m_loc,
        'OPTIONS': {
                    'username': _m_user,
                    'password': _m_pwd
            }
    }
}


# Change 'default' database configuration with $DATABASE_URL.
# Uncomment if use Postgres
_db_settings = dj_database_url.config(conn_max_age=500)
if not _db_settings:
    command = 'heroku config:get DATABASE_URL'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    _db_url, error = process.communicate()
    _db_settings = dj_database_url.parse(_db_url.decode().strip(), conn_max_age=500)

DATABASES['default'].update(_db_settings)


CELERY_BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL')
if CELERY_BROKER_URL is None:
    command = 'heroku config:get RABBITMQ_BIGWIG_URL'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    CELERY_BROKER_URL, error = process.communicate()

    CELERY_BROKER_URL = CELERY_BROKER_URL.decode().strip()
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
