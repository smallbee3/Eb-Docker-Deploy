


from .base import *


DEBUG = True
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.dev.application'
INSTALLED_APPS += [
    'django_extensions',
]



secrets = json.loads(open(SECRETS_DEV, 'rt').read())

set_config(secrets, module_name=__name__, start=True)
print(getattr(sys.modules[__name__], 'DATABASES'))


# 구 방식
# DATABASES = secrets['DATABASES']
