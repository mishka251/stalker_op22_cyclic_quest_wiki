from django.contrib.admin import ModelAdmin, register

from game_parser.models import Dialog
from game_parser.models.game_story import InfoPortion, TaskObjective
from game_parser.models.game_story.dialog import DialogPhrase
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class DialogsWhereNeeded(ReadOnlyNestedTable):
    model = Dialog.has_info.through
    verbose_name_plural = "Открывает диалоги"


class DialogsWhereGiving(ReadOnlyNestedTable):
    model = Dialog.give_info.through
    verbose_name_plural = "Получаем в диалогах"


class DialogPhrasesWhereGiving(ReadOnlyNestedTable):
    model = DialogPhrase.give_info.through
    verbose_name_plural = "Получаем во фразах диалогов"

class SetThenTaskObjectiveComplete(ReadOnlyNestedTable):
    model = TaskObjective
    verbose_name_plural = "Получаем при выполнении задания"
    fk_name = "infoportion_set_complete"

class SetThenTaskObjectiveFailing(ReadOnlyNestedTable):
    model = TaskObjective
    verbose_name_plural = "Получаем при провале задания"
    fk_name = "infoportion_set_fail"


class ThenTaskObjectiveComplete(ReadOnlyNestedTable):
    model = TaskObjective
    verbose_name_plural = "Получаем при выполнении задания(2)"
    fk_name = "infoportion_complete"





@register(InfoPortion)
class InfoPortionAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "game_id",
        # 'title_view',
    )

    search_fields = ["game_id"]
    autocomplete_fields = [
        "task",
        "actions",
    ]

    inlines = [
        DialogsWhereNeeded,
        DialogsWhereGiving,
        DialogPhrasesWhereGiving,
        SetThenTaskObjectiveComplete,
        SetThenTaskObjectiveFailing,
        ThenTaskObjectiveComplete,
    ]

__all__ = [
    "InfoPortionAdmin",
]