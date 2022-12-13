from game_parser.models.items.base_item import BaseItem
from django.db import models


class Artefact(BaseItem):
    class Meta:
        verbose_name = 'Базовый артефакт'
        verbose_name_plural = 'Артефакты/Капсулы аномалий/Эмбрионы мутантов'


class TrueArtefact(Artefact):
    class Meta:
        verbose_name = 'Артефакт'
        verbose_name_plural = 'Артефакты'

    inventory_radiation = models.DecimalField(decimal_places=6, max_digits=10, verbose_name='Радиоактивность',
                                              null=True)
    health_restore_speed = models.DecimalField(decimal_places=6, max_digits=10, verbose_name='Восстановление здоровья?',
                                               null=True)

    burn_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от ???', null=True)
    strike_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от ???', null=True)
    shock_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от ???', null=True)
    wound_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от ???', null=True)
    radiation_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от радиации', null=True)
    telepatic_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от телепатии', null=True)
    chemical_burn_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от химии', null=True)
    explosion_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от взрыва', null=True)
    fire_wound_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Защита от ???', null=True)
    power_restore_speed = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Восстановление сил', null=True)
    additional_weight = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Переносимый вес', null=True)
    radiation_restore_speed = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Радиация?', null=True)
    bleeding_restore_speed = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Кровотечение?', null=True)
    psy_health_restore_speed = models.DecimalField(decimal_places=5, max_digits=7, verbose_name='Пси-здоровье?', null=True)
    satiety_restore_speed = models.DecimalField(decimal_places=5, max_digits=7, verbose_name='???', null=True)
    jump_speed_delta = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Прыжок', null=True)


class MonsterEmbrion(Artefact):
    class Meta:
        verbose_name = 'Эмбрион мутанта'
        verbose_name_plural = 'Эмбрионы мутантов'


class CapsAnom(Artefact):
    class Meta:
        verbose_name = 'Капсула аномалии'
        verbose_name_plural = 'Капсулы аномалий'
