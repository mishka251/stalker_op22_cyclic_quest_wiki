from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import CycleTaskTarget, CycleTaskTargetStalker, CycleTaskTargetItem, \
    CycleTaskTargetCamp


@register(CycleTaskTarget)
class CycleTaskTargetAdmin(ModelAdmin):
    pass



@register(CycleTaskTargetCamp)
class CycleTaskTargetCampAdmin(ModelAdmin):
    pass

@register(CycleTaskTargetItem)
class CycleTaskTargetItemAdmin(ModelAdmin):
    pass

@register(CycleTaskTargetStalker)
class CycleTaskTargetStalkerAdmin(ModelAdmin):
    pass
