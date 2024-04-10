from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import Community, StalkerRank


@register(Community)
class CommunityAdmin(ModelAdmin):
    autocomplete_fields = [
        "translation"
    ]
    search_fields = [
        "name",
    ]


@register(StalkerRank)
class StalkerRankAdmin(ModelAdmin):
    autocomplete_fields = [
        "translation"
    ]

    search_fields = [
        "name",
    ]