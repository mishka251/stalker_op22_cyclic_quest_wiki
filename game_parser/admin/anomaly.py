from typing import Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import QuestRandomReward, Monster, EncyclopediaGroup, EncyclopediaArticle, Anomaly
from game_parser.models.quest import QuestRandomRewardThrough
from game_parser.utils.admin_utils.icon_view import icon_view
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable



@register(Anomaly)
class EncyclopediaGroupAdmin(ModelAdmin):
    autocomplete_fields = [
        'article',
    ]

    search_fields = [
        "section_name",
        "class_name",
    ]
    list_display = [
        "section_name",
        "class_name",
        "article",
    ]
