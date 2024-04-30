from django.contrib.admin import ModelAdmin, register

from game_parser.models.game_story import MoneyReward


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

__all__ = [
    "MoneyRewardAdmin",
]