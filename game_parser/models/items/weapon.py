from django.db import models

from game_parser.models.items.base_item import BaseItem


class Weapon(BaseItem):
    class Meta:
        verbose_name = 'Оружие'
        verbose_name_plural = 'Оружие'

    type = 'Weapon'
    ef_main_weapon_type = models.CharField(max_length=10, null=True)
    ef_weapon_type = models.CharField(max_length=10, null=True)
    weapon_class = models.CharField(max_length=255, null=True)
    ammo_mag_size = models.PositiveIntegerField(verbose_name='Размер магазина', null=True)
    fire_modes_str = models.CharField(max_length=255, verbose_name='Режимы стрельбы(сырая строка)', null=True)
    ammo_class_str = models.CharField(max_length=1000, verbose_name='Боеприпасы', null=True)
    grenade_class_str = models.CharField(max_length=1000, verbose_name='Типы гранат для подствольника', null=True)
    rpm = models.IntegerField(verbose_name='Скорострельность выстрелов в минуту', null=True)

    scope_status_str = models.CharField(max_length=5, verbose_name='Возможность установки прицела', null=True)
    silencer_status_str = models.CharField(max_length=5, verbose_name='Возможность установки глушителя', null=True)
    grenade_launcher_status = models.CharField(max_length=5, verbose_name='Возможность установки ГП', null=True)
    scope_name = models.CharField(max_length=255, verbose_name='Название прицела', null=True)
    silencer_name = models.CharField(max_length=255, verbose_name='Название глушителя', null=True)
    grenade_launcher_name = models.CharField(max_length=255, verbose_name='Название ГП', null=True)
    ammo_limit = models.PositiveIntegerField(verbose_name='???', null=True)
    ammo_elapsed = models.PositiveIntegerField(verbose_name='???', null=True)
    ammo_current = models.IntegerField(null=True)
    slot = models.IntegerField(null=True)

    scope = models.ForeignKey("Scope", on_delete=models.SET_NULL, null=True, verbose_name="Прицел")
    silencer = models.ForeignKey("Silencer", on_delete=models.SET_NULL, null=True, verbose_name="Глушитель")
    grenade_launcher = models.ForeignKey("GrenadeLauncher", on_delete=models.SET_NULL, null=True, verbose_name="Подствольник")
    ammo = models.ManyToManyField("Ammo", verbose_name="Патроны")
