from typing import Optional
from django.utils.safestring import mark_safe
from django.db.models.fields.files import ImageFieldFile

from game_parser.models import Icon


def icon_view(icon: ImageFieldFile) -> Optional[str]:
    if not icon:
        return None
    return mark_safe(f'<img src="{icon.url}" alt="{icon.name}">')
