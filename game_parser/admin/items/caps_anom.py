from django.contrib.admin import ModelAdmin, register

from game_parser.models import CapsAnom


@register(CapsAnom)
class CapsAnomAdmin(ModelAdmin):
    pass
