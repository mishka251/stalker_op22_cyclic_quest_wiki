from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import MapPosition


@register(MapPosition)
class MapPositionAdmin(ModelAdmin):
    autocomplete_fields = [
        "location",
    ]
    search_fields = [
        "name",
        "spawn_id",
        "story_id",
        "spawn_story_id",
    ]

    list_display = [
        "__str__",
        "name",
        "spawn_id",
        "story_id",
        "spawn_story_id",
    ]
