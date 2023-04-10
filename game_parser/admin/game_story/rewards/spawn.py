from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models.game_story import SpawnReward, TaskObjective, MapLocationType


@register(SpawnReward)
class SpawnRewardAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'function',
        'item_view',
        'xyz_raw',
    )

    @display(description='Предмет')
    def item_view(self, character: SpawnReward) -> str:
        return character.get_item
