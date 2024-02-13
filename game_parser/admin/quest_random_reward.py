from django.contrib.admin import ModelAdmin, register

from game_parser.models import QuestRandomReward
from game_parser.models.quest import QuestRandomRewardThrough
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class CyclicQuestRandomRewardInline(ReadOnlyNestedTable):
    model = QuestRandomRewardThrough
    verbose_name = 'Выдается в ЦЗ'
    verbose_name_plural = 'Выдается в ЦЗ'


@register(QuestRandomReward)
class QuestRandomRewardAdmin(ModelAdmin):
    autocomplete_fields = [
        'possible_items',
        "icon",
        "name_translation",
    ]

    search_fields = [
        "name",
        "caption",
    ]

    inlines = [
        CyclicQuestRandomRewardInline,
    ]
