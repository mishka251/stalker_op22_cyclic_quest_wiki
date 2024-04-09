from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import Community, StalkerRank


@register(Community)
class CommunityAdmin(ModelAdmin):
    pass


@register(StalkerRank)
class StalkerRankyAdmin(ModelAdmin):
    pass
