from django.contrib.admin import ModelAdmin, register

from game_parser.models import SpawnItem, NpcLogicConfig, CustomSpawnItem


@register(SpawnItem)
class SpawnItemAdmin(ModelAdmin):
    autocomplete_fields = [
        "item",
        "character_profile",
        "npc_logic",
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
        "location_txt",
        "game_vertex_id",
    ]

    list_filter = [
        "section_name",
        "location_txt",
    ]


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

