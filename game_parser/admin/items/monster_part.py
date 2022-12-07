from django.contrib.admin import ModelAdmin, register

from game_parser.models import MonsterPart


@register(MonsterPart)
class MonsterPartAdmin(ModelAdmin):
    pass
