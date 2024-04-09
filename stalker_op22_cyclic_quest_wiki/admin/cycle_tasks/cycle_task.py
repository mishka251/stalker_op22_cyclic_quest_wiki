from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import CyclicQuest


@register(CyclicQuest)
class CyclicQuestAdmin(ModelAdmin):
    autocomplete_fields = [
        "text",
        "vendor",
    ]

    search_fields = [
        "game_code",
    ]
