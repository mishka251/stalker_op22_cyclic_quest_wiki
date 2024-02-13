from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models.game_story import ItemReward, TaskObjective, MapLocationType


@register(ItemReward)
class ItemRewardAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'function',
        'count',
        'raw_count',
        'item',
        'raw_item',
    )

    autocomplete_fields = [
        "function",
        "item",
    ]

