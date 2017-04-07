"""
Django settings for RecipeWeekly project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


###################################################
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
###################################################

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '*_d2(56fg7e!)^0kvoake)7-vj0no=f1wqegzv#4suv2ev+8b^'
SECRET_KEY = os.environ['RECIPY_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
    'recipy.local',
]


###################################################
# Application definition
###################################################

INSTALLED_APPS = [
    'main.apps.MainConfig', # My app 
    'social_django', # Auth library for Facebook login
    'rest_framework', # Library for web API access

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware', 
]

ROOT_URLCONF = 'RecipeWeekly.urls'

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

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect', 
            ],
        },
    },
]

WSGI_APPLICATION = 'RecipeWeekly.wsgi.application'

AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.facebook.FacebookOAuth2',
)


###################################################
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
###################################################

DATABASES = {
    # Don't commit any sensitive information here
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Get Postgre database configuration from env var DATABASE_URL
db_from_env = dj_database_url.config(conn_max_age=500) 
DATABASES['default'].update(db_from_env)


###################################################
# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
###################################################

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


###################################################
# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
###################################################

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True


###################################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
###################################################

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')


###################################################
# Logging
# debug, info, warning, error, critical
###################################################

# DJANGO_LOG_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO', # os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG', 
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
        },
        # 'file': {
        #     'level': 'WARNING',
        #     'class': 'logging.FileHandler',
        #     'filename': BASE_DIR + '/logfile',
        #     'formatter': 'verbose',
        # },
    },

    'formatters': {
        'verbose': {
            # '()': 'djangocolors_formatter.DjangoColorsFormatter', # colored output
            'format': '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d %(thread)d %(pathname)s@%(lineno)s: %(message)s'
        },
        'simple': {
            # '()': 'djangocolors_formatter.DjangoColorsFormatter', # colored output
            'format': '%(levelname)s: %(message)s'
        },
    }
}


###################################################
# Login config
###################################################

LOGIN_URL = '/login/' # Redirected to login from login_required
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/' # After login when no next is specified


###################################################
# Facebook login 
###################################################

SOCIAL_AUTH_LOGIN_ERROR_URL = '/profile/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/profile/'
# SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_FACEBOOK_KEY = os.environ['RECIPY_SOCIAL_AUTH_FACEBOOK_KEY'] # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['RECIPY_SOCIAL_AUTH_FACEBOOK_SECRET'] # App Secret
# FACEBOOK_USER_TOKEN = 'EAAY79jQZCgaIBAAGhjiVSZASe2YI841eoEWMleIcZBb32ZBf00LwgeY7ZCQpLZChsXKFLZAZBf5YH38DMEJcTUNdivyJm6OZA4Y7kUp0GfX9s13zMij8bvzredKfgSrpjjUw4SWSa7FzFtvxTEmSWKo9P4IQgn00gVuGorg5HZBgA6IaxUi5gZA2rHx'
# FACEBOOK_APP_TOKEN = '1754778484834722|P_GiMG801m2HrBfriJ2OIXWBsiU'



###################################################
# Django Rest Framework 
###################################################
REST_FRAMEWORK = {
    'PAGE_SIZE': 50,
}

























