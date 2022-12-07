from django.contrib.admin import ModelAdmin, register

from game_parser.models import Grenade


@register(Grenade)
class GrenadeAdmin(ModelAdmin):
    pass
