from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models.game_story import GameTask, TaskObjective, MapLocationType

@register(GameTask)
class GameTaskAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'game_id',
        'title_view',
    )

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

    @display(description='Текст')
    def text_view(self, character: TaskObjective) -> str:
        return character.get_text

    @display(description='Запись')
    def article_view(self, character: TaskObjective) -> str:
        return character.get_article

@register(MapLocationType)
class MapLocationTypeAdmin(ModelAdmin):
    pass

