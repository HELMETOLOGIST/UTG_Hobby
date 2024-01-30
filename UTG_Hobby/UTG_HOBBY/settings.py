"""
Django settings for UTG_HOBBY project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x^5gb^x2l$7-*n%%874!$b^a85386jis9og_3e8h^seuqp=qxk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Google Authentication Area
SITE_ID = 5

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'phone'
        ],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'user_authentication',
    'user_products',
    'user_home',
    'user_cart',
    'user_profile',
    'user_order',
    'user_coupon',
    'user_wallet',
    'user_review',
    'admin_side',
    'django.contrib.humanize',
    
]



MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'UTG_HOBBY.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user_authentication.contextpro.username',
                'admin_side.contextadmin.adminame',
                'user_authentication.contextpro.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'UTG_HOBBY.wsgi.application'
AUTH_USER_MODEL = 'user_authentication.CustomUser'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "utg_hobby",
        "USER": "postgres",
        "PASSWORD": "nijith@2315",
        "HOST": "localhost",
        "PORT": "5432",
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIR = [
    os.path.join(BASE_DIR,'user_authentication/static'),
    os.path.join(BASE_DIR,'user_home/static'),
    os.path.join(BASE_DIR,'user_products/static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATIC_ROOT = os.path.join(BASE_DIR,'assets')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#### Email Verification
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nijithckv2001@gmail.com'
EMAIL_HOST_PASSWORD = 'ybrtwcnfqkzfggql'
# Set the default sender name
DEFAULT_FROM_EMAIL = 'UTG Hobby <nijithckv2001@gmail.com>'
# Login URL
LOGIN_URL = 'login'
#Session Engine
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
#Razorpay API Keys
RAZORPAY_API_KEY = config('RAZORPAY_API_KEY', default='rzp_test_uVOZmd57SunofW')
RAZORPAY_API_SECRET_KEY = config('RAZORPAY_API_SECRET_KEY', default='mfTY9FeuzBTeYGhZB0no3TRL')

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"


SOCIALACCOUNT_LOGIN_ON_GET=True

#Google Auth
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"



