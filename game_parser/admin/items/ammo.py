from django.contrib.admin import ModelAdmin, register

from game_parser.models import Ammo


@register(Ammo)
class AmmoAdmin(ModelAdmin):
    pass
