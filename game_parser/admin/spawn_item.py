from typing import Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import SpawnItem, NpcLogicConfig, CustomSpawnItem
from game_parser.utils.admin_utils.icon_view import icon_view


@register(SpawnItem)
class SpawnItemAdmin(ModelAdmin):
    autocomplete_fields = [
        "item",
        "character_profile",
        "npc_logic",
        "location",
    ]

    search_fields = [
        "section_name",
        "name",
        "spawn_id",
        "game_vertex_id",
    ]

    list_display = [
        "name",
        "section_name",
        "spawn_id",
        "location",
        "game_vertex_id",
        "position_raw",
        "map_bound_rect_raw",
        "inv_icon_view",
    ]

    list_filter = [
        "section_name",
        "location_txt",
    ]

    def _get_location_map(self, obj: SpawnItem) -> "Optional[LocationMapInfo]":
        if not obj.location:
            return None
        location_info = obj.location.locationmapinfo_set.first()
        return location_info

    @display(description='Иконка', )
    def inv_icon_view(self, obj: SpawnItem) -> Optional[str]:
        location_info = self._get_location_map(obj)
        if not location_info:
            return None
        return icon_view(location_info.map_image)

    @display(description='Границы локи', )
    def map_bound_rect_raw(self, obj: SpawnItem) -> Optional[str]:
        location_info = self._get_location_map(obj)
        if not location_info:
            return None
        return location_info.bound_rect_raw


@register(NpcLogicConfig)
class NpcLogicConfigAdmin(ModelAdmin):
    search_fields = [
        "name",
        "source_file_name",
    ]

    list_display = [
        "name",
        "source_file_name",
        "trade_file_name",
    ]

    autocomplete_fields = [
        "trade_config",
    ]


@register(CustomSpawnItem)
class CustomSpawnItemAdmin(ModelAdmin):
    autocomplete_fields = [
        "item",
        "character_profile",
        "npc_logic",
    ]

    search_fields = [
        "section_name",
        "name",
    ]

    list_display = [
        "name",
        "section_name",
    ]

    list_filter = [
        "section_name",
    ]

