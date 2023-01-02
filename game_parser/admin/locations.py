from django.contrib.admin import ModelAdmin, register

from game_parser.models import Location


@register(Location)
class LocationAdmin(ModelAdmin):
    pass
