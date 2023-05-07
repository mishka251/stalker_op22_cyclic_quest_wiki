from django.contrib.admin import ModelAdmin, register

from game_parser.models import CyclicQuest
from game_parser.models.quest import CyclicQuestItemReward, QuestRandomRewardThrough
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class CyclicQuestRewardInline(ReadOnlyNestedTable):
    model = CyclicQuestItemReward
    verbose_name = 'Награда'
    verbose_name_plural = 'Награды'


class CyclicQuestRandomRewardInline(ReadOnlyNestedTable):
    model = QuestRandomRewardThrough
    verbose_name = 'Случайная награда'
    verbose_name_plural = 'Случайные награды'


@register(CyclicQuest)
class QuestAdmin(ModelAdmin):
    autocomplete_fields = [
        'target_item',
        'random_rewards',
    ]

    inlines = [
        CyclicQuestRewardInline,
        CyclicQuestRandomRewardInline,
    ]

    search_fields = [
        "type",
        "game_code",
        "giver_code_local",
        "giver_code_global",
    ]


@register(QuestRandomRewardThrough)
class QuestRandomRewardThroughAdmin(ModelAdmin):
    autocomplete_fields = [
        'quest',
        'reward',
    ]

    search_fields = [
        'quest',
        'reward',
    ]
