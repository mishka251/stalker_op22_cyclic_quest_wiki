from django.db import models

from game_parser.models.items.base_item import BaseItem


class QuestRandomReward(models.Model):
    class Meta:
        verbose_name = 'Случайная награда за квест'
        verbose_name_plural = 'Случайные награды за квесты'

    name = models.CharField(max_length=255, verbose_name='Игровое название')
    caption = models.CharField(max_length=255, verbose_name='Человекочитабельное название', null=True)
    possible_items_str = models.CharField(max_length=2_000, verbose_name='Названия возможных предметов')
    possible_items = models.ManyToManyField(BaseItem, verbose_name='Возможные предметы')

    def __str__(self):
        if self.caption:
            return self.caption
        return self.name
   