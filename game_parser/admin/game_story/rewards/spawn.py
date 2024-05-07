from django.contrib.admin import ModelAdmin, display, register

from game_parser.models.game_story import SpawnReward


@register(SpawnReward)
class SpawnRewardAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "function",
        "item_view",
        "xyz_raw",
    )

    autocomplete_fields = [
        "item",
        "function",
    ]

    @display(description="Предмет")
    def item_view(self, character: SpawnReward) -> str:
        return character.get_item


__all__ = [
    "SpawnRewardAdmin",
]
