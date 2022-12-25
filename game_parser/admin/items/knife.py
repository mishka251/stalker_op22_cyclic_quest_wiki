from django.contrib.admin import ModelAdmin, register

from game_parser.admin.items.base_item_admin import BaseItemAdmin
from game_parser.models import Knife


@register(Knife)
class KnifeAdmin(BaseItemAdmin):
    list_display = (
        *BaseItemAdmin.list_display,
    )