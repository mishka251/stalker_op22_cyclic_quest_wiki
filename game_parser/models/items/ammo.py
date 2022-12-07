from django.db import models

from game_parser.models.items.base_item import BaseItem


class Ammo(BaseItem):
    type = 'Ammo'
