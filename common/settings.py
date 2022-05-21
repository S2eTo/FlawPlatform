"""
Django settings for common project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import mimetypes

from pathlib import Path
from django.core.management import utils

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = utils.get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'rest_framework',
    'dockerapi',
    'users',
    'v1'
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.CorsHeadersMiddleware',
    'common.middleware.RestFulSessionMiddleware',
    'common.middleware.RestFulCsrfViewMiddleware'
]

ROOT_URLCONF = 'common.urls'

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

WSGI_APPLICATION = 'common.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

DOCKER_API = {
    'URL': 'tcp://0.0.0.0:2375',
    # 外部映射地址, 只起到显示作用
    'EXTERNAL_URL': '0.0.0.0',
    # 映射端口区间如：30000-30500, 设置为 None 表示不设限制区间
    'PUBLIC_PORT_RANG': None,
    # 随机flag环境的 系统环境面过了名称
    'FLAG_ENVIRONMENT_NAME': 'RANDOM_FLAG',
    # 自动删除容器/靶机时间如: +1 为一小时后自动关闭
    'AUTO_REMOVE_CONTAINER': +1
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 头像文件后缀
VALID_IMAGE_FORMATS = ('jpg', )

# 头像最大大小
VALID_IMAGE_WIDTH = VALID_IMAGE_HEIGHT = 400


# Host for sending email.
EMAIL_HOST = 'smtp.exp.com'                 # 发送方的smtp服务器地址

# Port for sending email.
EMAIL_PORT = 587                           # smtp服务端口

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'xxx@exp.com'       # 发送方 邮箱地址
EMAIL_HOST_PASSWORD = 'xxx'                 # 获得的  授权码
EMAIL_USE_TLS = True                       # 必须为True
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None

# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 和 EMAIL_HOST_USER  相同

# 邮件激活码的过期时间，单位： 分钟。如下设置为 30 分钟
EMAIL_TOKEN_TIMEOUT = 30

# 注册邮件跳转地址
REGISTER_BASE_URI = 'http://0.0.0.0:8080'

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
