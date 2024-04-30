import os
import dj_database_url

from .base_settings import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""


DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL")
    )
}

STATIC_ROOT=BASE_DIR/"staticfiles"

sentry_sdk.init(
    dsn=...,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=0.5,
    enable_tracing=True,
    environment="production",
)
