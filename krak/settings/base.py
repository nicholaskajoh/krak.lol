"""
Django settings for Krak.lol.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.dirname(__name__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u^#!dw7h!#)g^1cw$7p2#206-zot02ka$=*yso^4sua192h_c_'

SITE_ID = 1

LOGIN_URL = '/?action=sign_in'

# Application definition

INSTALLED_APPS = [
  'api',
  'social', # main

  # 3rd party
  'anymail', # email
  'watson', # search
  'django_crontab', # cron jobs
  'admin_view_permission', # admin permissions
  'rest_framework', # api
  'rest_framework.authtoken', # api auth

  # django
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.sites',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.humanize',
]

MIDDLEWARE_CLASSES = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',

  'social.middleware.SetLastSeenMiddleware',
]

ROOT_URLCONF = 'krak.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': False,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'django.template.context_processors.media',
        'django.template.context_processors.i18n',
      ],
      'builtins': [
        'django.contrib.staticfiles.templatetags.staticfiles',
      ],
      'loaders': [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
      ],
    },
  },
]

WSGI_APPLICATION = 'krak.wsgi.application'

AUTHENTICATION_BACKENDS = (
  'krak.modules.backends.EmailOrUsernameModelBackend',
  'django.contrib.auth.backends.ModelBackend'
)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# STATIC_URL, route for static files
STATIC_URL = '/static/'
# STATIC_ROOT, 'collectstatic' copies static files here for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS, tuple of dirs with static files
# STATICFILES_DIRS = ()

# Media files (user-uploaded content)
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django crontab jobs
CRONJOBS = [
  ('0 0 1 * *', 'social.cron.login_to_site'),
  ('5 0 1 * *', 'social.cron.make_first_post'),
  ('0 0 * * 6', 'social.cron.account_notifications'),
  ('10 0 1 * *', 'social.cron.connect_with_others'),
]

# django admin view permissions
ADMIN_VIEW_PERMISSION_MODELS = [
  'auth.User',
  'social.Profile',
]

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.TokenAuthentication',
  )
}