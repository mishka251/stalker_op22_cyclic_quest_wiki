from django.db import models


class BaseItem(models.Model):
    visual_str = models.CharField(max_length=255, verbose_name='Название иконки?')
    description_code = models.CharField(max_length=255, verbose_name='Код названия(ссылка на переводы)')
    cost = models.PositiveIntegerField(verbose_name='Базовая цена')
    name = models.CharField(max_length=255, verbose_name='Название(код в игре)')

    inv_name = models.CharField(max_length=255, verbose_name='Название в инвентаре?', null=True)
    inv_name_short = models.CharField(max_length=255, verbose_name='Название в инвентаре(сокращенное)?', null=True)
    inv_weight = models.DecimalField(verbose_name='Вес', decimal_places=3, max_digits=6)
    cheat_item = models.BooleanField(default=False)
    quest_item = models.BooleanField(default=False, verbose_name='Квестовый предмет')

    def __str__(self):
        return self.name
