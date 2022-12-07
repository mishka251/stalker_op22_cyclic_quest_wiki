from django.contrib.admin import ModelAdmin, register

from game_parser.models import Silencer


@register(Silencer)
class SilencerAdmin(ModelAdmin):
    pass
