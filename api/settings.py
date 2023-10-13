################
import os
import logging
from pathlib import Path
from datetime import timedelta
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8&9_$w5wh3bcs*qn3tb9v-q3s#get-mg%fv)k_owb=hcx1=fjk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# HOST_SCHEME = "https://"
# # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = False
# SECURE_PROXY_SSL_HEADER = None
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000 
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True 
# SECURE_FRAME_DENY = True 
# SECURE_CONTENT_TYPE_NOSNIFF = True 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Library
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_extensions',
    'django_filters',

    # Applications
    'security',
    'smartmecanico',
    'employee_management',
    'smart_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
STATIC_ROOT = "/var/www/smartmecanico/static/"
MEDIA_ROOT = "/var/www/smartmecanico/media/"

STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'static/')
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
###################################################################
# Título da página de login
ADMIN_SITE_TITLE = 'Smart Mecânico'
INDEX_TITLE = "Adminstração Smart Mecânico"
ADMIN_SITE_HEADER = "Adminstração Smart Mecânico"

# SESSION 
SESSION_COOKIE_AGE = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# LOGGER DEBUG
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'], 
        'level': 'INFO',
    },
}

# NEW DATABASE CUSTOM
AUTH_USER_MODEL = 'security.CustomUser'

# URL
LOGOUT_REDIRECT_URL = '/admin/login/'

# SMTP SERVICES
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

# Cross-Origin Resource Sharing (CORS).
CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = [
    'http://138.255.232.130',
    'http://localhost:3000',
    'https://127.0.0.1',
    'http://127.0.0.1',
    'https://85.31.231.240',
    'http://85.31.231.240',
    'https://smartmecanico.app',
    'http://smartmecanico.app',
    'https://smart-api.smartmecanico.app',
    'http://smart-api.smartmecanico.app',
]

CSRF_TRUSTED_ORIGINS = [
    'http://138.255.232.130',
    'http://localhost:3000',
    'https://127.0.0.1',
    'http://127.0.0.1',
    'https://85.31.231.240',
    'http://85.31.231.240',
    'https://smartmecanico.app',
    'http://smartmecanico.app',
    'https://smart-api.smartmecanico.app',
    'http://smart-api.smartmecanico.app',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOWED_HEADERS = ['*']
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'API_TITLE': 'Smart Mecânico API V2',
    'API_DESCRIPTION': 'Agendamento de serviços mecânicos veiculares em qualquer lugar API',
    # 'EXCEPTION_HANDLER': 'security.utils.exception.custom_exception_handler',
    'NON_FIELD_ERRORS_KEY': "error",
}


# TOKEN SIMPLEJWT FOR DJANGO DRF
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=120),
    'SLIDING_TOKEN_REFRESH_LIFETIME_GRACE_PERIOD': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}