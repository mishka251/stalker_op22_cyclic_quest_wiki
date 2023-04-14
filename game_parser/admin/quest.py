from django.contrib.admin import ModelAdmin, register

from game_parser.models import CyclicQuest
from game_parser.models.quest import CyclicQuestItemReward
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class CyclicQuestRewardInline(ReadOnlyNestedTable):
    model = CyclicQuestItemReward
    verbose_name = 'Награда'
    verbose_name_plural = 'Награды'

@register(CyclicQuest)
class QuestAdmin(ModelAdmin):
    autocomplete_fields = [
        'target_item',
    ]

    inlines = [
        CyclicQuestRewardInline,
    ]