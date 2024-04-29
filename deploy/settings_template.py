import os
import dj_database_url

from .base_settings import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''


DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

STATIC_ROOT=BASE_DIR/"staticfiles"