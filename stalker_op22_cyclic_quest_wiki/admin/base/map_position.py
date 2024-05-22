from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import MapPosition


@register(MapPosition)
class MapPositionAdmin(ModelAdmin):
    autocomplete_fields = [
        "location",
    ]
    search_fields = [
        "location",
        "x",
        "y",
        "z",
    ]

    list_display = [
        "__str__",
        "location",
        "x",
        "y",
        "z",
    ]
