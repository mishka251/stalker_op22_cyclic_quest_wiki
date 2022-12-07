from django.contrib.admin import ModelAdmin, register

from game_parser.models import Knife


@register(Knife)
class KnifeAdmin(ModelAdmin):
    pass
