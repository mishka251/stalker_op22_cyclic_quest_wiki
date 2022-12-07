from django.contrib.admin import ModelAdmin, register

from game_parser.models import Weapon


@register(Weapon)
class WeaponAdmin(ModelAdmin):
    pass
