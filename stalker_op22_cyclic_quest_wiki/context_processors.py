import os

from django.http import HttpRequest


def use_sentry_js(request: HttpRequest) -> dict:
    should_use_sentry_js = bool(os.getenv("SENTRY_DSN"))
    return {
        "use_sentry_js": should_use_sentry_js,
    }
