from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import Item


@register(Item)
class ItemAdmin(ModelAdmin):
    pass
