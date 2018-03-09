"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import importlib
import json
import numbers
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
# SECRETS_BASE = json.loads(open(SECRETS_DIR, 'rt').read())
# SECRETS_LOCAL = os.path.join(SECRETS_DIR, 'local.json')
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')
SECRETS_LOCAL = os.path.join(SECRETS_DIR, 'local.json')

secrets = json.loads(open(SECRETS_BASE, 'rt').read())


# # SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets["SECRET_KEY"]



def set_config(obj, start=False):
    """
    Python객체를 받아, 해당 객체의 key-value쌍을
    현재 모듈(config.settings.base)에 동적으로 할당
    1. dict거나 list일 경우에는 내부 값들이 eval()이 가능한지 검사해야 함
    2. value가 dict나 list가 아닐 경우에는
        2-1. eval()이 가능하다면 해당 결과를 할당
        2-2. eval()이 불가능하다면 (일반 텍스트나 숫자일 경우) 값 자체를 할당
    :param obj:
    :return:
    """

    def eval_obj(obj):
        """
        주어진 파이썬 객체의 타입에 따라 eval()결과를 반환하거나 불가한 경우 그냥 그 객체를 반환
        1. 그대로 반환
            - int, float형이거나 str형이며 숫자 변환이 가능한 경우에는 그대로 반환
            - eval()에서 예외가 발생했으며 없는 변수를 참조할때의 NameError가 발생한 경우
        2. eval() 평가값을 반환
            - 1번의 경우가 아니며 eval()이 가능한 경우 평가값을 반환
        3. 그대로 반환하되, 로그를 출력
            - 1번의 경우가 아니며 eval()에서 NameError외의 예외가 발생한 경우
        :param obj: 파이썬 객체
        :return: eval(obj)또는 obj
        """
        # 객체가 int, float거나
        if isinstance(obj, numbers.Number) or (
                # str형이면서 숫자 변환이 가능한 경우
                isinstance(obj, str) and obj.isdigit()):
            return obj

        # 객체가 int, float가 아니면서 숫자형태를 가진 str도 아닐경우
        try:
            return eval(obj)
        except NameError:
            # 없는 변수를 참조할 때 발생하는 예외
            return obj
        except Exception as e:
            print(f'Cannot eval object({obj}), Exception: {e}')
            return obj
            # raise ValueError(f'Cannot eval object({obj}), Exception: {e}')

    # base.json파일을 parsing한 결과 (Python dict)를 순회
    # set_config에 전달된 객체가 'dict'형태일 경우
    if isinstance(obj, dict):
        # key, value를 순회
        for key, value in obj.items():
            # value가 dict거나 list일 경우 재귀적으로 함수를 다시 실행
            if isinstance(value, dict) or isinstance(value, list):
                set_config(value)
            # 그 외의 경우 value를 평가한 값을 할당
            else:
                obj[key] = eval_obj(value)
            # set_config()가 처음 호출된 loop에서만 setattr()을 실행
            if start:
                setattr(sys.modules[__name__], key, value)
    # 전달된 객체가 'list'형태일 경우
    elif isinstance(obj, list):
        # list아이템을 순회하며
        for index, item in enumerate(obj):
            # list의 해당 index에 item을 평가한 값을 할당
            obj[index] = eval(item)


# set_config에서 'raven'모듈을 필요로 하나, 이 모듈의 다른 부분에서 사용하지 않음
# import raven이라고 쓸 경우 Code reformating에서 필요없는 import로 인식해서 지워짐
# raven모듈을 importlib를 사용해 가져온 후 현재 모듈에 'raven'이라는 이름으로 할당
setattr(sys.modules[__name__], 'raven', importlib.import_module('raven'))
set_config(secrets, start=True)

print(f'SECRET_KEY: {getattr(sys.modules[__name__], "SECRET_KEY")}')
print(f'RAVEN_CONFIG: {getattr(sys.modules[__name__], "RAVEN_CONFIG")}')



# def set_config(obj, start=False):
#     """
#     Python객체를 받아, 해당 객체의 key-value쌍을
#     현재 모듈(config.settings.base)에 동적으로 할당
#
#     :param obj:
#     :return:
#     """
#     #
#     # for i, j in obj.items():
#     #     key = i
#     #     value = j
#     #     i = str(j)
#     #     # print(f'i: {i}')
#     #     # print(f'j: {j}')
#     #     # print(f'key: {key}')
#     #     # print(key)
#     #     # key = eval(i)
#     #     # value = eval(j)
#     #     if type(i) != dict:
#     #         print(eval(i))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'






# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Thirdparty App
    'django_extensions',
    'raven.contrib.django.raven_compat',

    # Custom App

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

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]




# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Google에서 django sentry log 검색 후 처음 문서
# https://docs.sentry.io/clients/python/integrations/django/

# (* Google에서 django sentry로 검색 후 나오는 처음 문서와 이유는 모르나
#   처음 부분에 내용이 조금 다름)
#   https://raven.readthedocs.io/en/stable/integrations/django.html

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
