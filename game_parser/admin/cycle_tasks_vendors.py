from typing import Optional

from django.contrib.admin import ModelAdmin, display, register

from game_parser.models import CycleTaskVendor


@register(CycleTaskVendor)
class CycleTaskVendorAdmin(ModelAdmin):
    search_fields = (
        "game_story_id_raw",
        "vendor_id",
    )

    list_display = (
        "__str__",
        "game_story_id_raw",
        "vendor_id",
        "game_story_id",
        "get_spawn_section",
        "get_npc_profile",
    )

    autocomplete_fields = [
        "game_story_id",
    ]

    @display(description="Секция спавна")
    def get_spawn_section(self, obj: CycleTaskVendor) -> str | None:
        spawn_section = obj.get_spawn_section()
        if not spawn_section:
            return None
        return str(spawn_section)

    @display(description="Профиль НПС")
    def get_npc_profile(self, obj: CycleTaskVendor) -> str | None:
        npc_profile = obj.get_npc_profile()
        if not npc_profile:
            return None
        return str(npc_profile)
