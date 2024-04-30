from django.contrib.admin import ModelAdmin, register
from polymorphic.admin import PolymorphicInlineSupportMixin

from game_parser.models import BaseScriptReward, InfoPortion, ItemReward, MoneyReward, SpawnReward
from game_parser.models.game_story import ScriptFunction
from game_parser.models.game_story.dialog import DialogPhrase
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable, ReadOnlyPolymorphicChildInline, ReadOnlyPolymorphicInline


class RewardsInline(ReadOnlyPolymorphicInline):
    model = BaseScriptReward

    class SpawnRewardInline(ReadOnlyPolymorphicChildInline):
        model = SpawnReward
        autocomplete_fields = [
            "item",
        ]

    class MoneyRewardInline(ReadOnlyPolymorphicChildInline):
        model = MoneyReward

    class ItemRewardInline(ReadOnlyPolymorphicChildInline):
        model = ItemReward
        autocomplete_fields = [
            "item",
        ]

    child_inlines = (
        SpawnRewardInline,
        MoneyRewardInline,
        ItemRewardInline,
    )

class DialogPhrasesCallsFunction(ReadOnlyNestedTable):
    model = DialogPhrase.actions.through
    verbose_name = "Используется в фразах диалогов"

class InfoportionCallsFunction(ReadOnlyNestedTable):
    model = InfoPortion.actions.through
    verbose_name = "Используется в инфопоршнях"


@register(ScriptFunction)
class ScriptFunctionAdmin(PolymorphicInlineSupportMixin, ModelAdmin):
    list_display = (
        "__str__",
        "name",
        "namespace",
        "dialog",
        # 'nested_function',
        # 'raw_nested_function',
        "rewards",
    )
    inlines = (
        RewardsInline,
        DialogPhrasesCallsFunction,
        InfoportionCallsFunction,
    )
    search_fields = [
        "namespace",
        "name",
    ]

    autocomplete_fields = [
        "dialog",
        "nested_function",
    ]

    def rewards(self, func: ScriptFunction) -> str:
        return "\n".join([str(reward) for reward in func.rewards.all()])

__all__ = [
    "ScriptFunctionAdmin",
]
