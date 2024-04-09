from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor


@register(CycleTaskVendor)
class CycleTaskVendorAdmin(ModelAdmin):
    pass
