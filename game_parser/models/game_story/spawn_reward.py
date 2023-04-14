from game_parser.models import BaseItem
from game_parser.models.game_story.base_script_reward import BaseScriptReward
from django.db import models

import dataclasses
import decimal
import os
import re
from decimal import Decimal
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
import logging

from luaparser.ast import ASTVisitor, FloatDivOp,Op, Call, Number, String, parse, Index, to_lua_source, Nil, Name, Function, UnaryOp, Invoke



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
    def parse_raw(self) -> Call:
        tree = parse(self.raw_call)
        call = tree.body.body[0]
        return call

    @property
    def is_spawn_in_inventory(self) -> bool:
        return len(self.parse_raw.args) == 5

    @property
    def spawn_target(self):
        if self.is_spawn_in_inventory:
            return f'Объект {to_lua_source(self.parse_raw.args[-1])}'
        else:
            return f'Координаты {self.get_coords}'
