from game_parser.models.items.base_item import BaseItem


class Grenade(BaseItem):
    class Meta:
        verbose_name = "Граната"
        verbose_name_plural = "Гранаты"

    type = "Grenade"
