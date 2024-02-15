from django.db import models

from game_parser.models import Translation
from game_parser.models.items.base_item import BaseItem


class Treasure(models.Model):
    class Meta:
        verbose_name = 'Тайник'
        verbose_name_plural = 'Тайники'

    target = models.CharField(null=False, max_length=10, verbose_name='spawn_id для поиска в спавне')
    name_str = models.CharField(null=False, max_length=255, verbose_name='Название(код перевода)')
    description_str = models.CharField(null=False, max_length=255, verbose_name='Описание(код перевода)')
    items_str = models.CharField(null=False, max_length=1_000, verbose_name='Предметы в тайнике(строкой)')
    condlist_str = models.CharField(null=False, max_length=1_000, verbose_name='Условия')
    custom_name = models.CharField(null=True, max_length=255, verbose_name='Название(2)(код перевода)')

    custom_name_translation = models.ForeignKey(
        Translation,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Перевод названия',
        related_name='+'
    )
    description_translation = models.ForeignKey(
        Translation,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Перевод описания',
        related_name='+'
    )

    spawn_item = models.ForeignKey("SpawnItem", null=True, on_delete=models.SET_NULL, verbose_name="Секция спавна")


    def __str__(self):
        treasure_str = ''
        if self.custom_name_translation:
            treasure_str += self.custom_name_translation.rus
        treasure_str += f' {self.name_str} {self.target}'
        return treasure_str


class ItemInTreasure(models.Model):
    class Meta:
        verbose_name = 'Предмет в тайнике'
        verbose_name_plural = 'Предметы в тайниках'

    item = models.ForeignKey(BaseItem,  null=False, on_delete=models.CASCADE, verbose_name='Предмет')
    treasure = models.ForeignKey(Treasure,  null=False, on_delete=models.CASCADE, verbose_name='Тайник')
    count = models.PositiveIntegerField(verbose_name='Кол-во предметов', default=1)

    def __str__(self):
        return f'{self.count} {self.item} в {self.treasure}'
