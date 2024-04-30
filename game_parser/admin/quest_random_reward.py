from typing import Any, Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import QuestRandomReward
from game_parser.models.quest import QuestRandomRewardThrough
from game_parser.utils.admin_utils.icon_view import icon_view
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class CyclicQuestRandomRewardInline(ReadOnlyNestedTable):
    model = QuestRandomRewardThrough
    verbose_name = "Выдается в ЦЗ"
    verbose_name_plural = "Выдается в ЦЗ"


class RandomRewardItemInline(ReadOnlyNestedTable):
    model = QuestRandomReward.possible_items.through
    verbose_name = "Предметы"
    verbose_name_plural = "Предметы"
    readonly_fields = [
        "name_translation_rus",
        "inv_icon_view",
    ]

    @display(description="Название")
    def name_translation_rus(self, obj: Any) -> str:
        obj = obj.baseitem
        if obj.name_translation:
            return obj.name_translation.rus
        return obj.inv_name

    @display(description="Иконка", )
    def inv_icon_view(self, obj: Any) -> Optional[str]:
        obj = obj.baseitem
        return icon_view(obj.inv_icon)


@register(QuestRandomReward)
class QuestRandomRewardAdmin(ModelAdmin):
    autocomplete_fields = [
        "possible_items",
        "icon",
        "name_translation",
    ]

    search_fields = [
        "name",
        "caption",
    ]

    inlines = [
        RandomRewardItemInline,
        CyclicQuestRandomRewardInline,
    ]

    list_display = [
        "__str__",
        "inv_icon_view",
    ]

    @display(description="Иконка", )
    def inv_icon_view(self, obj: QuestRandomReward) -> Optional[str]:
        if obj.icon:
            return icon_view(obj.icon.icon)
        return None
