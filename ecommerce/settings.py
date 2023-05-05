import mimetypes
from pathlib import Path
import os
import dj_database_url
from decouple import config
from django.core.management.utils import get_random_secret_key

mimetypes.add_type("text/css", ".css", True)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

APPEND_SLASH=False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'store',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600),
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/images/'

MEDIA_ROOT='BASE_DIR/"static/images"'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PAYPAL_RECEIVER_EMAIL = config('PAYPAL_RECEIVER_EMAIL')

PAYPAL_TEST = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# set SECURE_HSTS_SECONDS to a non-zero value to enable HSTS
SECURE_HSTS_SECONDS = 315300 # or any value that you prefer

# set SECURE_SSL_REDIRECT to True to enforce SSL connection
SECURE_SSL_REDIRECT = True

# set SECURE_HSTS_INCLUDE_SUBDOMAINS to True if all subdomains should be served via SSL
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# set SECURE_HSTS_PRELOAD to True to submit your site to the browser preload list
SECURE_HSTS_PRELOAD = True

# set SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE to True to use secure-only cookies
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECRET_KEY = get_random_secret_key()
