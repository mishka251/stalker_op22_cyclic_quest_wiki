from django.contrib.admin import ModelAdmin, display, register

from game_parser.admin.utils import SpawnItemMapRenderer
from game_parser.models import CampInfo, CustomSpawnItem, NpcLogicConfig, Respawn, SingleStalkerSpawnItem, SpawnItem, StalkerSection
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


    @display(description="Карта" )
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



@register(CampInfo)
class CampInfoAdmin(ModelAdmin):
    autocomplete_fields = [
        "spawn_item",
        "communities",
    ]

    list_display = [
        "spawn_item",
        "type",
        "communities_raw",
        "cond_raw",
    ]

    search_fields = [
        "type",
        "spawn_item__name",
    ]


@register(Respawn)
class RespawnAdmin(ModelAdmin):
    autocomplete_fields = [
        "spawn_item",
        "respawn_section",
    ]

    list_display = [
        "spawn_item",
        "respawn_section_raw",
    ]

    search_fields = [
        "spawn_item__name",
    ]

@register(SingleStalkerSpawnItem)
class SingleStalkerSpawnItemAdmin(ModelAdmin):
    autocomplete_fields = [
        "spawn_item",
        "stalker_section",
    ]

    list_display = [
        "spawn_item",
        "character_profile_raw",
        "stalker_section",
    ]

    search_fields = [
        "character_profile_raw",
        "spawn_item__name",
    ]


class RespawnsInline(ReadOnlyNestedTable):
    model = Respawn.respawn_section.through

class SingleStalkerSpawnItemInline(ReadOnlyNestedTable):
    model = SingleStalkerSpawnItem


@register(StalkerSection)
class StalkerSectionAdmin(ModelAdmin):
    autocomplete_fields = [
        "character_profile",
        "community",
    ]

    list_display = [
        "section_name",
        "character_profile_str",
        "community_str",
        "community",
        "character_profile",
    ]

    search_fields = [
        "section_name",
        "community_str",
    ]

    inlines = [
        RespawnsInline,
        SingleStalkerSpawnItemInline,
    ]
