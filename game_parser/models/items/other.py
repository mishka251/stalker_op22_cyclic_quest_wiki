from game_parser.models.items.base_item import BaseItem


class Other(BaseItem):
    class Meta:
        verbose_name = 'Прочий предмет'
        verbose_name_plural = 'Прочее'

    type = 'Other'
