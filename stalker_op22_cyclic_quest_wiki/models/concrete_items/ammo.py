from django.db import models

from stalker_op22_cyclic_quest_wiki.models.base.base_item import Item


class Ammo(Item):
    class Meta:
        verbose_name = "Боеприпас"
        verbose_name_plural = "Боеприпасы"

    box_size = models.PositiveIntegerField(verbose_name="Кол-во патронов в пачке?")


__all__ = [
    "Ammo",
]
