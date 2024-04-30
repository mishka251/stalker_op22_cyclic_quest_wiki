from typing import Optional

from django.db.models.fields.files import ImageFieldFile
from django.utils.safestring import mark_safe


def icon_view(icon: ImageFieldFile) -> Optional[str]:
    if not icon:
        return None
    return mark_safe(f'<img src="{icon.url}" alt="{icon.name}">')
