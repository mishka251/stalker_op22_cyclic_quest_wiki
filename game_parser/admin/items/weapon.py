from django.contrib.admin import register

from game_parser.admin.items.base_item_admin import BaseItemAdmin
from game_parser.models import Weapon
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class AmmoInline(ReadOnlyNestedTable):
    model = Weapon.ammo.through


@register(Weapon)
class WeaponAdmin(BaseItemAdmin):
    list_display = (
        *BaseItemAdmin.list_display,
    )

    inlines = [
        *BaseItemAdmin.inlines,
        AmmoInline,
    ]

    autocomplete_fields = [
        *BaseItemAdmin.autocomplete_fields,
        'ammo',
        'grenade_launcher',
        'scope',
        'silencer',
    ]
