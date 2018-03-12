


from .base import *


DEBUG = True
ALLOWED_HOSTS = []
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
STATICFILES_STORAGE = 'config.storages.StaticStorage'
