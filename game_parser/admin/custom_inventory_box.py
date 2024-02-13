from django.contrib.admin import  ModelAdmin, register

from game_parser.models import InventoryBox, ItemInTreasureBox


@register(InventoryBox)
class InventoryBoxAdmin(ModelAdmin):
    search_fields = [
        "section_name",
    ]

@register(ItemInTreasureBox)
class ItemInTreasureBoxAdmin(ModelAdmin):
    autocomplete_fields = [
        "box",
        "item",
    ]
