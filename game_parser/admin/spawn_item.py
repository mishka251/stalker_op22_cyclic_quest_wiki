import re
from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.template import loader

from game_parser.admin.utils import SpawnItemMapRenderer
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


    @display(description='Карта', )
    def map(self, obj: SpawnItem) -> str:
        renderer = SpawnItemMapRenderer(obj)
        return renderer.render()


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
        "custom_inventory_box",
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

