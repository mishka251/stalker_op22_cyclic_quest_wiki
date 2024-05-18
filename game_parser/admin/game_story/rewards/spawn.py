from django.contrib.admin import ModelAdmin, display, register

from game_parser.admin.utils import SpawnRewardMapRenderer
from game_parser.models import CustomSpawnItem
from game_parser.models.game_story import SpawnReward


@register(SpawnReward)
class SpawnRewardAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "function",
        "item_view",
        "xyz_raw",
        "custom_section_view",
        "game_vertex_obj",
        "map_view",
    )

    autocomplete_fields = [
        "item",
        "function",
        "custom_spawn_section",
        "game_vertex_obj",
    ]

    search_fields = [
        "raw_maybe_item",
        "raw_target",
        "raw_call",
    ]

    @display(description="Предмет")
    def item_view(self, obj: SpawnReward) -> str:
        return obj.get_item

    @display(description="Кастомная секция", ordering="custom_spawn_section_id")
    def custom_section_view(self, obj: SpawnReward) -> CustomSpawnItem | None:
        return obj.custom_spawn_section

    @display(description="Карта")
    def map_view(self, obj: SpawnReward) -> str | None:
        renderer = SpawnRewardMapRenderer(obj)
        return renderer.render()


__all__ = [
    "SpawnRewardAdmin",
]
