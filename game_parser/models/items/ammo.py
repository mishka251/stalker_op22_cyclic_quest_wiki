from django.db import models

from game_parser.models.items.base_item import BaseItem


class Ammo(BaseItem):
    class Meta:
        verbose_name = 'Боеприпас'
        verbose_name_plural = 'Боеприпасы'

    type = 'Ammo'
