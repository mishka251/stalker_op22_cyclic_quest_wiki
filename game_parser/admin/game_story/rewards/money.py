from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models.game_story import MoneyReward, TaskObjective, MapLocationType


@register(MoneyReward)
class MoneyRewardAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'function',
        'count',
        'raw_count',
    )

    autocomplete_fields = [
        "function",
    ]
