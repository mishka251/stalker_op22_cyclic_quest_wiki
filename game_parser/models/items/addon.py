from game_parser.models.items.base_item import BaseItem


class Addon(BaseItem):
    class Meta:
        verbose_name = 'Обвес'
        verbose_name_plural = 'Обвесы'

    type = 'Addon'
