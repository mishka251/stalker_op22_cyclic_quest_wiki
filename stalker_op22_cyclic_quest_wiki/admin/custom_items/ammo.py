from django.contrib.admin import register, ModelAdmin

from stalker_op22_cyclic_quest_wiki.models import Ammo


@register(Ammo)
class AmmoAdmin(ModelAdmin):
    autocomplete_fields = [
        "description_translation",
        "icon",
        "name_translation",
    ]
    search_fields = [
        "name",
    ]
