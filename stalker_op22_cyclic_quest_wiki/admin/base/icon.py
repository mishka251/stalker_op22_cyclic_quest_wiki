from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import Icon


@register(Icon)
class IconAdmin(ModelAdmin):
    search_fields = [
        "name",
    ]
