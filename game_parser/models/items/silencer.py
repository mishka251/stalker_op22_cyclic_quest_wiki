from game_parser.models.items.addon import Addon
from django.db import models

class Silencer(Addon):
    class Meta:
        verbose_name = 'Глушитель'
        verbose_name_plural = 'Глушители'

    condition_shot_dec = models.DecimalField(verbose_name='знос за 1 выстрел', decimal_places=8, max_digits=12, null=True)
