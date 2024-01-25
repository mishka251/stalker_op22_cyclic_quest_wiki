from typing import Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import Location, LocationMapInfo
from game_parser.utils.admin_utils.icon_view import icon_view


@register(Location)
class LocationAdmin(ModelAdmin):
    autocomplete_fields = [
        "name_translation",
    ]
    search_fields = [
        "game_id",
        "game_code",
        "name",
    ]

@register(LocationMapInfo)
class LocationMapInfoAdmin(ModelAdmin):
    autocomplete_fields = [
        "location",
    ]
    list_display = [
        "location",
        "name",
        "map_image",
        "inv_icon_view",
    ]

    @display(description='Иконка', )
    def inv_icon_view(self, obj: LocationMapInfo) -> Optional[str]:
        return icon_view(obj.map_image)
