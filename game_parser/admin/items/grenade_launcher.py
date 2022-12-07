from django.contrib.admin import ModelAdmin, register

from game_parser.models import GrenadeLauncher


@register(GrenadeLauncher)
class GrenadeLauncherAdmin(ModelAdmin):
    pass
