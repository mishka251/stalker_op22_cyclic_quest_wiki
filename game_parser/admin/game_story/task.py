from django.contrib.admin import ModelAdmin, register, display

from game_parser.models.game_story import GameTask, TaskObjective, MapLocationType
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class TaskObjectiveInline(ReadOnlyNestedTable):
    model = TaskObjective


@register(GameTask)
class GameTaskAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'game_id',
        'title_view',
    )

    inlines = [
        TaskObjectiveInline,
    ]

    search_fields = ['game_id']
    autocomplete_fields = [
        "title",
    ]

    @display(description='Имя')
    def title_view(self, character: GameTask) -> str:
        return character.get_title


@register(TaskObjective)
class TaskObjectiveAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'task',
        'text_view',
        'article_view',
    )

    autocomplete_fields = [
        "icon",
        "task",
        "text",
        "function_complete",
        "infoportion_complete",
        "infoportion_set_complete",
        "function_fail",
        "infoportion_set_fail",
        "function_call_complete",
        "article",
    ]

    search_fields = [
        "task",
        "text_id_raw",
    ]

    @display(description='Текст')
    def text_view(self, character: TaskObjective) -> str:
        return character.get_text

    @display(description='Запись')
    def article_view(self, character: TaskObjective) -> str:
        return character.get_article

@register(MapLocationType)
class MapLocationTypeAdmin(ModelAdmin):
    autocomplete_fields = [
        "hint",
        "objective",
    ]


__all__ = [
    "GameTaskAdmin",
    "TaskObjectiveAdmin",
    "MapLocationTypeAdmin",
]
