from django.contrib.admin import ModelAdmin, register

from game_parser.models import GameStoryId


@register(GameStoryId)
class GameStoryIdAdmin(ModelAdmin):
    search_fields = (
        "story_id",
        "section_name",
    )

    list_display = (
        "__str__",
        "story_id",
        "section_name",
        "spawn_section",
        "spawn_section_custom",
    )

    autocomplete_fields = [
        "item",
        "treasure",
        "character",
        "spawn_section",
        "spawn_section_custom",
    ]
