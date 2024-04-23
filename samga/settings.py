"""
Django settings for samga project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

from pathlib import Path
import os

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6aqu8h+-u))26sf4*8-v0!rmbb=sswtls$up4d=h5$5m!*8jp8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'samga.onrender.com',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'academy',
    'django_cleanup',
    'widget_tweaks',    
    'crispy_forms',
    'django.contrib.humanize',
    'cloudinary_storage',
    'cloudinary',
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
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'samga.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'samga.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    #}

    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #    'NAME': 'samga',
    #    'USER' : 'customer',
    #    'PASSWORD' : 'customer',
    #    'HOST' : '127.0.0.1',
    #    'PORT' : '5432',
    #}    

    'default': {
	    'ENGINE': 'django.db.backends.postgresql_psycopg2',
	    'NAME': 'shop_mc1t',
	    'USER' : 'shop_admin',
	    'PASSWORD' : 'JoY0YbPaAPPWheCcNZFZOGpTQMX4P5nT',
	    'HOST' : 'dpg-cojsa88cmk4c73c2ndd0-a.frankfurt-postgres.render.com',
	    'PORT' : '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGES = (
    ('kk', 'Kazakh'),
    ('ru', 'Russian'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
#]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Для работы с медиафайлами
MEDIA_URL = '/ media /'
MEDIA_ROOT = os.path.join (BASE_DIR, 'media')

# установить Bootstrap 4 в качестве структуры стилей по умолчанию для django-crispy-forms:
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
# Теперь, при входе в систему, вы по умолчанию должны перенаправляться на домашнюю страницу сайта а не на /accounts/profile/
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGOUT_URL = '/'

#Сохранения изображения
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dwvyooc7m',
    'API_KEY': '268241926117228',
    'API_SECRET': 'uvcsfjn54MH3R6xdc-lPhcXuk9w',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Сброс пароля по E-Mail
EMAIL_TIMEOUT = 300

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'shop260222@mail.ru' 
EMAIL_HOST_PASSWORD = 'Nn27t2PMDiJ7rSqWeFuw'
DEFAULT_FROM_EMAIL  = 'shop260222@mail.ru'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

