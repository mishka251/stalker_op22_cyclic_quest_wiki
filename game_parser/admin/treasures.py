from typing import Optional

from django.contrib.admin import ModelAdmin, display, register

from game_parser.models import ItemInTreasure, Treasure
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class TreasureItemsAdmin(ReadOnlyNestedTable):
    model = ItemInTreasure


@register(Treasure)
class TreasureAdmin(ModelAdmin):
    search_fields = (
        "name_str",
        "custom_name",
    )

    list_display = (
        "__str__",
        "name_str",
        "description_view",
        "custom_name_view",
    )

    autocomplete_fields = [
        "custom_name_translation",
        "description_translation",
        "spawn_item",
    ]

    inlines = [
        TreasureItemsAdmin,
    ]

    @display(description="Описание", ordering="description_translation__rus")
    def description_view(self, treasure: Treasure) -> str:
        return treasure.description_translation.rus if treasure.description_translation else treasure.description_str

    @display(description="Название(кастомное?)", ordering="custom_name_translation__rus")
    def custom_name_view(self, treasure: Treasure) -> str | None:
        return treasure.custom_name_translation.rus if treasure.custom_name_translation else treasure.custom_name
