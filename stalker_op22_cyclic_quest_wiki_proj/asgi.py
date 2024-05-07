"""
ASGI config for stalker_op22_cyclic_quest_wiki_proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "stalker_op22_cyclic_quest_wiki_proj.settings",
)

application = get_asgi_application()
