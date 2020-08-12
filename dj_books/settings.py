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
from django.urls import reverse_lazy

## Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dr@0-#9nj4=loa8)j_5(s&m7s=fbmlo=15yeac01q#kiij$cev'

## @note SECURITY WARNING: don't run with debug turned on in production!
## Defines is a Debug environment
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1' ]


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
    'django.middleware.locale.LocaleMiddleware', #Must be here
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
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
                'books.context_processors.my_context', 
            ],
        },
    },
]


WSGI_APPLICATION = 'dj_books.wsgi.application'

from sys import path
path.append("dj_books/reusing/")
from myconfigparser import MyConfigParser
myconfigparser=MyConfigParser("/etc/dj_books/settings.conf")
## Database connection definitions
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': myconfigparser.get("db", "db", "mylibrary"),
        'USER': myconfigparser.cget("db", "user", "postgres"),
        'PASSWORD': myconfigparser.cget("db", "password", "mypass"),
        'HOST': myconfigparser.get("db", "server", "127.0.0.1"),
        'PORT': myconfigparser.getInteger("db", "port", 5432),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = myconfigparser.get("smtp", "server", "127.0.0.1")
EMAIL_PORT = myconfigparser.getInteger("smtp", "port", 25)
EMAIL_HOST_USER = myconfigparser.cget("smtp", "user",  "user")
EMAIL_HOST_PASSWORD =myconfigparser.cget("smtp", "password",  "mypass")
EMAIL_USE_TLS = myconfigparser.getBoolean("smtp", "tls",  False)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

#print(f"Smtp server: smtp://{EMAIL_HOST_USER}@{EMAIL_HOST}:{EMAIL_PORT} (Tls: {EMAIL_USE_TLS})")


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
LANGUAGES=[
    ("en", "English"),  
    ("es",  "Español"), 
    ("fr", "Français") , 
    ("ro", "Romanian"), 
    ("ru", "Russian"), 
]
## Timezone definition
TIME_ZONE = 'UTC'

## Allos internationalization
USE_I18N = True

USE_L10N = False
DATE_FORMAT = "Y-m-d"

USE_TZ = True
LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGOUT_REDIRECT_URL = reverse_lazy("login")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR+ "/books/static/"

## Sets session timeout in seconds.
SESSION_COOKIE_AGE = 600

## Session cookie age is renewed in every request
SESSION_SAVE_EVERY_REQUEST = True

## Expires session if browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

