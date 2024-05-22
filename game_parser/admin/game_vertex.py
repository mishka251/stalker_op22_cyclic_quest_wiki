from django.contrib.admin import ModelAdmin, register

from game_parser.models import GameVertex


@register(GameVertex)
class GameVertexAdmin(ModelAdmin):
    autocomplete_fields = [
        "location",
    ]

    list_display = [
        "__str__",
        "vertex_id",
        "location",
    ]

    search_fields = [
        "vertex_id",
    ]
