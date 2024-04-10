from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import CycleTaskTarget, CycleTaskTargetStalker, CycleTaskTargetItem, \
    CycleTaskTargetCamp


@register(CycleTaskTarget)
class CycleTaskTargetAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
    ]


@register(CycleTaskTargetCamp)
class CycleTaskTargetCampAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
        "map_position",
    ]


@register(CycleTaskTargetItem)
class CycleTaskTargetItemAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
        "item",
    ]


@register(CycleTaskTargetStalker)
class CycleTaskTargetStalkerAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
        "map_positions",
        "community",
        "rank",
    ]
