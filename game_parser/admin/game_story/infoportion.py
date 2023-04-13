from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models import Dialog
from game_parser.models.game_story import InfoPortion, TaskObjective, MapLocationType
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class DialogsWhereNeeded(ReadOnlyNestedTable):
    model = Dialog.has_info.through
    verbose_name_plural = 'Открывает диалоги'


class DialogsWhereGiving(ReadOnlyNestedTable):
    model = Dialog.give_info.through
    verbose_name_plural = 'Получаем в диалогах'


@register(InfoPortion)
class InfoPortionAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'game_id',
        # 'title_view',
    )

    search_fields = ['game_id']
    autocomplete_fields = [
        'task',
        'actions',
    ]

    inlines = [
        DialogsWhereNeeded,
        DialogsWhereGiving,
    ]
