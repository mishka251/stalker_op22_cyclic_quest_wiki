from game_parser.models import BaseItem
from game_parser.models.game_story.base_script_reward import BaseScriptReward
from django.db import models


class SpawnReward(BaseScriptReward):
    class Meta:
        ...
    item = models.ForeignKey(BaseItem, verbose_name='Предмет', null=True, on_delete=models.SET_NULL)
    raw_maybe_item = models.CharField(max_length=512, null=False) # МБ заспавнен не предмет, а НПС или мутант
    raw_call = models.CharField(max_length=512, null=False) # спавн сложнее, сохраним всю строку

    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)

    raw_level_vertex = models.CharField(max_length=512, null=False)
    raw_game_vertex_id = models.CharField(max_length=512, null=False)

    level_vertex = models.IntegerField(null=True)
    game_vertex_id = models.IntegerField(null=True)

    xyz_raw = models.CharField(max_length=512, null=False) # спавн сложнее, сохраним всю строку
    raw_target = models.CharField(max_length=512, null=True) # спавн сложнее, сохраним всю строку
