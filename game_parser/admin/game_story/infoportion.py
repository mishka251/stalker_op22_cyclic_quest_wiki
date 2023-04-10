from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models.game_story import InfoPortion, TaskObjective, MapLocationType

@register(InfoPortion)
class InfoPortionAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'game_id',
        # 'title_view',
    )

    search_fields = ['game_id']
