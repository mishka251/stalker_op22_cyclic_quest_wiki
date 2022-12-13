from django.contrib.admin import ModelAdmin, register

from game_parser.models import MonsterEmbrion


@register(MonsterEmbrion)
class MonsterEmbrionAdmin(ModelAdmin):
    pass
