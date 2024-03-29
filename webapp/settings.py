"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from channels.sessions import SessionMiddlewareStack


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)h74h*q%8nsh8g7j!xvflbw+qa^j4!4hg4c8ass&7y26lg0l7f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'daphne' ,
   
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'app',
    'channels',
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    

    
    
    
]

 


ROOT_URLCONF = "webapp.urls"

TEMPLATES = [
    {
         
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [BASE_DIR / 'templates/app'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webapp.wsgi.application"
ASGI_APPLICATION = 'webapp.asgi.application'



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Địa chỉ máy chủ SMTP của Gmail
EMAIL_PORT = 587  # Cổng của máy chủ SMTP (TLS)
EMAIL_USE_TLS = True  # Sử dụng TLS (True/False tùy thuộc vào cài đặt của bạn)
EMAIL_HOST_USER = 'chaugiathinh2020@gmail.com'  # Thay bằng địa chỉ email của bạn
EMAIL_HOST_PASSWORD = 'dcro zmvj rbco ulmp'  # Thay bằng mật khẩu ứng dụng bạn vừa tạo

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR,'app/static/images')

ASGI_APPLICATION = 'webapp.asgi.application'
CHANNEL_LAYERS = {
	"default": {
		"BACKEND": "channels.layers.InMemoryChannelLayer"
	}
}
