from django.db import models

from game_parser.models.items.base_item import BaseItem


class Ammo(BaseItem):
    class Meta:
        verbose_name = 'Боеприпас'
        verbose_name_plural = 'Боеприпасы'

    type = 'Ammo'

    box_size = models.PositiveIntegerField(verbose_name='Кол-во патронов в пачке?')
    k_dist = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    k_disp = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    k_hit = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    k_impulse = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    k_pierce = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    impair = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    wm_size = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    tracer_str = models.CharField(max_length=5, null=True)
    explosive_str = models.CharField(max_length=5, null=True)
    buck_shot = models.PositiveIntegerField(verbose_name='Дроби в выстреле?', null=True)
