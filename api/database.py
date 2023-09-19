import os
from decouple import config

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': config('DB_NAME', os.path.join(os.path.dirname(__file__), 'db.sqlite3')),
    # },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', '172.16.0.10'),
        'PORT': config('DB_PORT', '3306'),
    },
    # 'postgresql': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': config('DB_NAME'),
    #     'USER': config('DB_USER'),
    #     'PASSWORD': config('DB_PASSWORD'),
    #     'HOST': config('DB_HOST', '172.16.0.10'),
    #     'PORT': config('DB_PORT', '5432'),
    # },
    # 'oracle': {
    #     'ENGINE': 'django.db.backends.oracle',
    #     'NAME': config('DB_NAME'),
    #     'USER': config('DB_USER'),
    #     'PASSWORD': config('DB_PASSWORD'),
    #     'HOST': config('DB_HOST', '172.16.0.10'),
    #     'PORT': config('DB_PORT', '1521'),
    # },
    # 'sql_server': {
    #     'ENGINE': 'django.db.backends.mssql',
    #     'NAME': config('DB_NAME'),
    #     'USER': config('DB_USER'),
    #     'PASSWORD': config('DB_PASSWORD'),
    #     'HOST': config('DB_HOST', '172.16.0.10'),
    #     'PORT': config('DB_PORT', '1433'),
    # },
}
