from typing import Optional

from django.contrib.admin import display, register

from game_parser.admin.items.base_item_admin import BaseItemAdmin
from game_parser.models import Monster, MonsterPart
from game_parser.utils.admin_utils.icon_view import icon_view
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class MonsterInline(ReadOnlyNestedTable):
    model = Monster
    fields = [
        "name_translation",
        "section_name",
        "short_name",
        "class_name",
        "Spawn_Inventory_Item_Probability",
        "inv_icon_view",
    ]

    readonly_fields = [
        "inv_icon_view",
    ]

    @display(description="Иконка" )
    def inv_icon_view(self, obj: Monster) -> str | None:
        if not obj.icon:
            return None
        return icon_view(obj.icon.icon)


@register(MonsterPart)
class MonsterPartAdmin(BaseItemAdmin):
    list_display = (
        *BaseItemAdmin.list_display,
    )

    inlines = [
        *BaseItemAdmin.inlines,
        MonsterInline,
    ]
