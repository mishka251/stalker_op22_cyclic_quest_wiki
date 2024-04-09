from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import Translation


@register(Translation)
class TranslationAdmin(ModelAdmin):
    pass
