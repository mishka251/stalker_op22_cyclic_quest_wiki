from django.contrib.admin import ModelAdmin, register

from game_parser.models import Explosive


@register(Explosive)
class ExplosiveAdmin(ModelAdmin):
    pass
