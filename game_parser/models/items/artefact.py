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

    inventory_radiation = models.DecimalField(decimal_places=6, max_digits=10, verbose_name='Радиоактивность(из рюкзака)',
                                              null=True)
    health_restore_speed = models.DecimalField(decimal_places=6, max_digits=10, verbose_name='Восстановление здоровья',
                                               null=True)

    burn_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Ожог', null=True)
    strike_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Удар', null=True)
    shock_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Электрошок', null=True)
    wound_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Разрыв', null=True)
    radiation_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='защита от радиации', null=True)
    telepatic_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Телепатии', null=True)
    chemical_burn_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Химический ожог', null=True)
    explosion_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Взрыв', null=True)
    fire_wound_immunity = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Пулестойкость', null=True)
    power_restore_speed = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Восстановление сил', null=True)
    additional_weight = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Переносимый вес', null=True)
    radiation_restore_speed = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Вывод радиации из организма', null=True)
    bleeding_restore_speed = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Кровотечение', null=True)
    psy_health_restore_speed = models.DecimalField(decimal_places=5, max_digits=7, verbose_name='Пси-здоровье?', null=True)
    satiety_restore_speed = models.DecimalField(decimal_places=5, max_digits=7, verbose_name='Насыщение', null=True)
    jump_speed_delta = models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Прыжок', null=True)


class MonsterEmbrion(Artefact):
    class Meta:
        verbose_name = 'Эмбрион мутанта'
        verbose_name_plural = 'Эмбрионы мутантов'


class CapsAnom(Artefact):
    class Meta:
        verbose_name = 'Капсула аномалии'
        verbose_name_plural = 'Капсулы аномалий'
