## @package settings
##Django settings for dj_books project.
##
##Generated by 'django-admin startproject' using Django 1.11.2.
##
##For more information on this file, see
##https://docs.djangoproject.com/en/1.11/topics/settings/
##
##For the full list of settings and their values, see
##https://docs.djangoproject.com/en/1.11/ref/settings/

import os

## Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dr@0-#9nj4=loa8)j_5(s&m7s=fbmlo=15yeac01q#kiij$cev'

## @note SECURITY WARNING: don't run with debug turned on in production!
## Defines is a Debug environment
DEBUG = True

ALLOWED_HOSTS = ['localhost', ]


## Application definitions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'books',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'dj_books.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+"/templates/"],
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

WSGI_APPLICATION = 'dj_books.wsgi.application'


## Database connection definitions
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mylibrary',
        'USER': 'postgres',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
django_send_mail=open("/etc/django_send_mail", "r").read().split("\t")
EMAIL_HOST_USER = django_send_mail[0]
EMAIL_HOST_PASSWORD =django_send_mail[1]
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


## Locale paths in source distribution
LOCALE_PATHS = (
    BASE_DIR+ '/locale/',
)

## Password validation 
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

## Language code
LANGUAGE_CODE = 'en-us'

## Timezone definition
TIME_ZONE = 'UTC'

## Allos internationalization
USE_I18N = True

USE_L10N = False
DATE_FORMAT = "Y-m-d"

USE_TZ = True
LOGIN_REDIRECT_URL = './'
LOGOUT_URL = "./"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/dj_books/static/'
STATIC_ROOT = BASE_DIR+ "/static"

## Sets session timeout in seconds.
SESSION_COOKIE_AGE = 600

## Session cookie age is renewed in every request
SESSION_SAVE_EVERY_REQUEST = True

## Expires session if browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

