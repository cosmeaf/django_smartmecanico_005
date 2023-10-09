import os
from pathlib import Path
from decouple import config
from datetime import timedelta
from api.database import DATABASES


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

#ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])
ALLOWED_HOSTS = ['*']


HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# Application definition
INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Library
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'django_extensions',

    # Applications
    'security',
    'address',
    'vehicle',
    'services',
    'appointment',
    'employee_management',
]

MIDDLEWARE = [    
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.common.CommonMiddleware',    
    'corsheaders.middleware.CorsMiddleware',
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

DATABASES['default'] = DATABASES['default']


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
#########################################################

# LOGGER


# AUTHENTICATION BACKENDS
AUTHENTICATION_BACKENDS = [
    'security.authentication.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Cross-Origin Resource Sharing (CORS).
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    'https://85.31.231.240',
    'http://85.31.231.240',
    'https://localhost:8000',
    'http://localhost:8000',
    'https://127.0.0.1:8000',
    'http://127.0.0.1:8000'
]
CSRF_TRUSTED_ORIGINS = ["https://api-smartmecanico.dockersky.com"]
CSRF_ALLOWED_ORIGINS = ["https://api-smartmecanico.dockersky.com"]
CORS_ORIGINS_WHITELIST = ["https://api-smartmecanico.dockersky.com"]
CORS_ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
CORS_ALLOWED_HEADERS = ['*']
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# SMTP SERVICES
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

# DJANGO REST FRAMEWORK ACCESS AND PERMISSIONS
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
    'API_DESCRIPTION': 'Agendamento de serviços mecânicos veícular em qualquer lugar API',
}

# DJANGO SIMPLE JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}
