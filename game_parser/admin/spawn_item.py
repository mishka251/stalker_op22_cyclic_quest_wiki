import re
from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.template import loader

from game_parser.models import SpawnItem, NpcLogicConfig, CustomSpawnItem, LocationMapInfo
from game_parser.utils.admin_utils.icon_view import icon_view
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


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
        "map",
    ]

    list_filter = [
        "section_name",
        "location_txt",
    ]

    readonly_fields = [
        "map",

    ]

    def _get_location_map(self, obj: SpawnItem) -> "Optional[LocationMapInfo]":
        if not obj.location:
            return None
        location_info = obj.location.locationmapinfo_set.first()
        return location_info

    @display(description='Карта', )
    def map(self, obj: SpawnItem) -> str:
        location = obj.location
        location_info = LocationMapInfo.objects.get(location=location)
        offset_re = re.compile(r"\s*(?P<min_x>.*),\s*(?P<min_y>.*),\s*(?P<max_x>.*),\s*(?P<max_y>.*)")
        rm = offset_re.match(location_info.bound_rect_raw)
        (min_x, min_y, max_x, max_y) = (
            float(rm.group("min_x")),
            float(rm.group("min_y")),
            float(rm.group("max_x")),
            float(rm.group("max_y"))
        )

        y_level_offset = -(max_y + min_y)
        context = {
            "item": self._spawn_item_to_dict(obj),
            "item_var_name": f"item_{obj.id}",
            "map_offset": (min_x, min_y, max_x, max_y),
            "map_offset_name": f"map_offset_{obj.id}",
            "y_level_offset": y_level_offset,
            "y_level_offset_name": f"y_level_offset_{obj.id}",
            "layer_image_url": location_info.map_image.url,
            "item_id": str(obj.id),
        }
        return loader.render_to_string("leaflet_map_field.html", context)

    def _spawn_item_to_dict(self, spawn_item: SpawnItem) -> dict:
        position_re = re.compile(r"\s*(?P<x>.*),\s*(?P<y>.*),\s*(?P<z>.*)")
        rm = position_re.match(spawn_item.position_raw)
        if not rm:
            return None
        (x, y, z) = float(rm.group("x")), float(rm.group("y")), float(rm.group("z"))
        position = (x, z)
        name = spawn_item.name
        section_name = spawn_item.section_name

        return {
            "position": position,
            "name": name,
            "section_name": section_name,
        }


class SpawnItemInline(ReadOnlyNestedTable):
    model = SpawnItem


class CustomSpawnItemInline(ReadOnlyNestedTable):
    model = CustomSpawnItem


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

    inlines = [
        SpawnItemInline,
        CustomSpawnItemInline,
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

