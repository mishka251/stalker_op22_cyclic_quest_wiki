from django.contrib.admin import ModelAdmin, register

from game_parser.models import CyclicQuest


@register(CyclicQuest)
class QuestAdmin(ModelAdmin):
    pass
