from .base import *


DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.elasticbeanstalk.com',
]
WSGI_APPLICATION = 'config.wsgi.dev.application'
INSTALLED_APPS += [
    'django_extensions',
    'storages',
]

secrets = json.loads(open(SECRETS_DEV, 'rt').read())

set_config(secrets, module_name=__name__, start=True)
print(getattr(sys.modules[__name__], 'DATABASES'))


# 구 방식
# DATABASES = secrets['DATABASES']


# AWS S3관련 설정
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

# Static files(collectstatic)를 위한 스토리지
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# 3/15 주석처리 한 이유:
# S3대신 EC2에서 정적파일을 제공 (프리티어의 Put사용량 절감)
# 없으면 기본값이 들어가니까 주석처리만 하면 끝

# STATICFILES_STORAGE = 'config.storages.StaticStorage'
