from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import Location, LocationMapInfo


@register(Location)
class LocationAdmin(ModelAdmin):
    autocomplete_fields = [
        "map_info",
        "name_translation",
    ]

    search_fields = [
        "name",
    ]


@register(LocationMapInfo)
class LocationMapInfoAdmin(ModelAdmin):
    search_fields = [
        "location_name",
    ]
