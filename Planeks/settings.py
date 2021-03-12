import os

import django_heroku
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_REDIRECT_URL = 'workpalce'
LOGOUT_REDIRECT_URL = 'workpalce'

SECRET_KEY = 'DEBUG-+q=8f=)x&0_vmmb%tf_ykb_cemy7u)51tcea-3gimedtwevfny'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'workplace.apps.WorkplaceConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Planeks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Planeks.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'planeks',
        'USER': 'godbd',
        'PASSWORD': 'Answer42!',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'Planeks/static/',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

if DEBUG:
    # REDIS related settings
    CELERY_REDIS_HOST = 'localhost'
    CELERY_REDIS_PORT = '6379'
    CELERY_BROKER_URL = 'redis://' + CELERY_REDIS_HOST + ':' + CELERY_REDIS_PORT + '/0'
    CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
    CELERY_RESULT_BACKEND = 'redis://' + CELERY_REDIS_HOST + ':' + CELERY_REDIS_PORT + '/0'
else:
    django_heroku.settings(locals())
    BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
