from django.contrib.admin import ModelAdmin, register

from game_parser.models import InventoryBox, ItemInTreasureBox
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class ItemInTreasureBoxInline(ReadOnlyNestedTable):
    model = ItemInTreasureBox


@register(InventoryBox)
class InventoryBoxAdmin(ModelAdmin):
    search_fields = [
        "section_name",
    ]

    inlines = [
        ItemInTreasureBoxInline,
    ]



@register(ItemInTreasureBox)
class ItemInTreasureBoxAdmin(ModelAdmin):
    autocomplete_fields = [
        "box",
        "item",
    ]
