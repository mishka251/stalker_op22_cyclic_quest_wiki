from django.db import models

from game_parser.models.items.base_item import BaseItem
from game_parser.models.game_story.base_script_reward import BaseScriptReward


class SpawnReward(BaseScriptReward):
    class Meta:
        ...
    item = models.ForeignKey(BaseItem, verbose_name='Предмет', null=True, on_delete=models.SET_NULL)
    raw_maybe_item = models.CharField(max_length=512, null=False) # МБ заспавнен не предмет, а НПС или мутант
    raw_call = models.TextField(max_length=2048, null=False) # спавн сложнее, сохраним всю строку

    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)

    raw_level_vertex = models.CharField(max_length=512, null=False)
    raw_game_vertex_id = models.CharField(max_length=512, null=False)

    level_vertex = models.IntegerField(null=True)
    game_vertex_id = models.IntegerField(null=True)

    xyz_raw = models.CharField(max_length=512, null=False) # спавн сложнее, сохраним всю строку
    raw_target = models.CharField(max_length=512, null=True) # спавн сложнее, сохраним всю строку

    @property
    def get_coords(self):
        if self.x and self.y and self.z:
            return f'{self.x} {self.y} {self.z}'
        return self.xyz_raw

    @property
    def get_item(self) -> str:
        if self.item:
            return str(self.item)
        return self.raw_maybe_item

    def __str__(self):
        return f'Спавн {self.get_item} в {self.spawn_target}'

    @property
    def is_spawn_in_inventory(self) -> bool:
        return bool(self.raw_target)

    @property
    def spawn_target(self):
        if self.is_spawn_in_inventory:
            return f'Объект {self.raw_target}'
        else:
            return f'Координаты {self.get_coords}'
