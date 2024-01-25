from typing import Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import GameStoryId
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


@register(GameStoryId)
class GameStoryIdAdmin(ModelAdmin):
    search_fields = (
        'story_id',
        'section_name',
    )

    list_display = (
        '__str__',
        'story_id',
        'section_name',
        'spawn_section',
        'spawn_section_custom',
    )

    autocomplete_fields = [
        'item',
        'treasure',
        'character',
        'spawn_section',
        'spawn_section_custom',
    ]
