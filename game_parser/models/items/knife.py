from django.db import models

from game_parser.models.items.base_item import BaseItem


class Knife(BaseItem):
    class Meta:
        verbose_name = 'Нож'
        verbose_name_plural = 'Ножи'

    type = 'Knife'
