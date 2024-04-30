from django.contrib.admin import register

from game_parser.admin.items.base_item_admin import BaseItemAdmin
from game_parser.models import Ammo


@register(Ammo)
class AmmoAdmin(BaseItemAdmin):
    list_display = (*BaseItemAdmin.list_display,)
