from django.db import models

from game_parser.models.items.addon import Addon


class GrenadeLauncher(Addon):
    class Meta:
        verbose_name = 'Подствольный гранатомёт'
        verbose_name_plural = 'Подствольные гранатомёты'

    type = 'GrenadeLauncher'

    ammo_class_str = models.CharField(max_length=255, null=True, verbose_name='Боеприпас')
