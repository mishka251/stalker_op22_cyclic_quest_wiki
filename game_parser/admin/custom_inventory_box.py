from django.contrib.admin import  ModelAdmin, register

from game_parser.models import InventoryBox, ItemInTreasureBox


@register(InventoryBox)
class InventoryBoxAdmin(ModelAdmin):
    pass

@register(ItemInTreasureBox)
class ItemInTreasureBoxAdmin(ModelAdmin):
    pass
