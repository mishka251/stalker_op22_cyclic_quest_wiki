from django.contrib.admin import ModelAdmin, register

from game_parser.models import QuestRandomReward


@register(QuestRandomReward)
class QuestRandomRewardAdmin(ModelAdmin):
    filter_horizontal = [
        'possible_items',
    ]
