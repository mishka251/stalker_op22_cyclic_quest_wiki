from django.contrib.admin import ModelAdmin, register

from game_parser.models import Addon


@register(Addon)
class AddonAdmin(ModelAdmin):
    pass
