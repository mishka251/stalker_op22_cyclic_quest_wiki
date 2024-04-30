from typing import Optional

from django.contrib.admin import ModelAdmin, display, register

from game_parser.models import CyclicQuest, StorylineCharacter
from game_parser.models.quest import CyclicQuestItemReward, QuestRandomRewardThrough
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class CyclicQuestRewardInline(ReadOnlyNestedTable):
    model = CyclicQuestItemReward
    verbose_name = "Награда"
    verbose_name_plural = "Награды"


class CyclicQuestRandomRewardInline(ReadOnlyNestedTable):
    model = QuestRandomRewardThrough
    verbose_name = "Случайная награда"
    verbose_name_plural = "Случайные награды"


@register(CyclicQuest)
class QuestAdmin(ModelAdmin):
    autocomplete_fields = [
        "target_item",
        "target_stalker",
        "target_camp_to_destroy",
        "target_camp_to_defeat",
        "target_camp",
        "vendor",
        "text",
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

    list_filter = [
        "type",
        "giver_code_local",
        "giver_code_global",
    ]

    list_display = [
        "__str__",
        "type",
        "get_vendor_character",
        "prior",
        "target_camp",
        "target_camp_to_destroy",
        "target_camp_to_defeat",
        "target_stalker",
    ]

    @display(description="Квестодатель")
    def get_vendor_character(self, obj: CyclicQuest) -> "StorylineCharacter | None":
        return obj.get_vendor_character


@register(QuestRandomRewardThrough)
class QuestRandomRewardThroughAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
        "reward",
    ]

    search_fields = [
        "quest",
        "reward",
    ]
