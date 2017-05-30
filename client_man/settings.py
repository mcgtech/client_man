"""
Django settings for client_man project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8*h5-t7fpqr&dcx9ki(5rbxdq!2&@s11-$+$)3+m_v(hpxy#0q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_pagination',
    'widget_tweaks',
    'django_tables2',
    'crispy_forms',
    'common',
    'client',
    'constance.backends.database',
    'constance',
]
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'GEN_FROM_EMAIL_ADDRESS': ('mcgonigalstephen@gmail.com', 'General From Address'),
    'ACCEPTANCE_EMAIL_LIST': ('mcgonigalstephen@gmail.com', 'Who to email on acceptance'),
    'REVOKE_EMAIL_LIST': ('mcgonigalstephen@gmail.com', 'Who to email on revoking'),
    'APPROVAL_EMAIL_LIST': ('mcgonigalstephen@gmail.com', 'Who to email on approval'),
    'REJECT_EMAIL_LIST': ('mcgonigalstephen@gmail.com', 'Who to email on rejection'),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'General Options': ('GEN_FROM_EMAIL_ADDRESS',),
    'Contract Options': ('ACCEPTANCE_EMAIL_LIST', 'REVOKE_EMAIL_LIST', 'APPROVAL_EMAIL_LIST', 'REJECT_EMAIL_LIST'),
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'client_man.urls'

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
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'client_man.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'client_management',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-GB'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# http://stackoverflow.com/questions/25593038/django-static-folder-not-in-the-base-project
STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'static'))

STATIC_URL = '/static/' # You may find this is already defined as such.

STATICFILES_DIRS = (
STATIC_PATH,
)
LOGIN_URL = 'client_man_login'
LOGOUT_URL = 'client_man_logout'
LOGIN_REDIRECT_URL = '/client_search'

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATE_INPUT_FORMATS = ('%d/%m/%Y')
#DATE_INPUT_FORMATS = ('%d/%m/%Y','%Y-%m-%d')

DISPLAY_DATE = '%d/%m/%Y'
DISPLAY_DATE_TIME = '%d/%m/%Y %H:%M:%S'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

# Global constants
# groups
ADMIN_GROUP = 'admin'
CLIENT_GROUP = 'client'
JOB_COACH = 'job coach'
JOB_COACH_MAN = 'job coach manager'
INFO_MAN = 'info manager'
PARTNER = 'partner'
SUPPLY_CHAIN_MAN = 'supply chain manager'
SUPPLY_CHAIN_PART = 'supply chain partner'

# Message types
INFO_MSG_TYPE = 0
SUCC_MSG_TYPE = 1
WARN_MSG_TYPE = 2
ERR_MSG_TYPE = 3
DEBUG_MSG_TYPE = 4

# status approval
DISPLAY_APPROVE = 0
DISPLAY_REJECT = 1
DISPLAY_REVOKE = 2
DISPLAY_ACCEPT = 4

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
# https://github.com/jakubroztocil/django-settings-export
# allows us to access constants inside templates
SETTINGS_EXPORT = [
    'ADMIN_GROUP',
    'CLIENT_GROUP',
    'JOB_COACH',
    'JOB_COACH_MAN',
    'INFO_MAN',
    'PARTNER',
    'SUPPLY_CHAIN_MAN',
    'SUPPLY_CHAIN_PART',
    'INFO_MSG_TYPE',
    'SUCC_MSG_TYPE',
    'WARN_MSG_TYPE',
    'ERR_MSG_TYPE',
    'DEBUG_MSG_TYPE'
]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}