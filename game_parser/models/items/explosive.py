from game_parser.models.items.base_item import BaseItem


class Explosive(BaseItem):
    class Meta:
        verbose_name = "Взрывчатка"
        verbose_name_plural = "Взрывчатка"

    type = "Explosive"
