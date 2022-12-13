from django.contrib.admin import ModelAdmin, register

from game_parser.models import Outfit


@register(Outfit)
class OutfitAdmin(ModelAdmin):
    pass
