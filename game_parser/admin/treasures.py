from typing import Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import Treasure


@register(Treasure)
class TreasureAdmin(ModelAdmin):
    search_fields = (
        'name_str',
        'custom_name',
    )

    list_display = (
        '__str__',
        'name_str',
        'description_view',
        'custom_name_view',
    )

    @display(description='Описание', ordering='description_translation__rus')
    def description_view(self, treasure: Treasure) -> str:
        return treasure.description_translation.rus if treasure.description_translation else treasure.description_str

    @display(description='Название(кастомное?)', ordering='custom_name_translation__rus')
    def custom_name_view(self, treasure: Treasure) -> Optional[str]:
        return treasure.custom_name_translation.rus if treasure.custom_name_translation else treasure.custom_name