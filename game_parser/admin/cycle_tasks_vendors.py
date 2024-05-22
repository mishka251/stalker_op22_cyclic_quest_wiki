from django.contrib.admin import ModelAdmin, display, register
from django.utils.safestring import mark_safe

from game_parser.admin.utils import SpawnItemMapRenderer, SpawnRewardMapRenderer
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
        "map",
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

    @display(description="Карта")
    def map(self, obj: CycleTaskVendor) -> str | None:
        spawn_item = obj.get_spawn_item()
        rendered_maps = []
        if spawn_item is not None:
            renderer = SpawnItemMapRenderer(spawn_item)
            rendered_map = renderer.render()
            if rendered_map:
                rendered_maps.append(rendered_map)

        rewards = obj.get_spawn_rewards()

        maybe_rendered_maps = [
            SpawnRewardMapRenderer(spawn_reward).render() for spawn_reward in rewards
        ]
        rendered_maps.extend(
            rendered_map
            for rendered_map in maybe_rendered_maps
            if rendered_map is not None
        )
        if rendered_maps:
            return mark_safe("\n\n".join(rendered_maps))
        return None
