from django.contrib.admin import ModelAdmin, register

from game_parser.models.game_story import ItemReward


@register(ItemReward)
class ItemRewardAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "function",
        "count",
        "raw_count",
        "item",
        "raw_item",
    )

    autocomplete_fields = [
        "function",
        "item",
    ]


__all__ = [
    "ItemRewardAdmin",
]
