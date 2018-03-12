from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    # 3/8 정엽님 조언으로 캐치.
    default_acl = 'public-read'
