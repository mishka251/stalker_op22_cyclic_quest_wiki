from django.db import models

from game_parser.models.items.base_item import BaseItem


class Outfit(BaseItem):
    class Meta:
        verbose_name_plural = "Броня"
        verbose_name = "Броня"

    burn_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от огня?"
    )
    strike_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от ???"
    )
    shock_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от ???"
    )
    wound_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от ???"
    )
    radiation_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от радиации"
    )
    telepatic_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от телепатии"
    )
    chemical_burn_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от химии"
    )
    explosion_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от взрыва"
    )
    fire_wound_protection = models.DecimalField(
        decimal_places=4, max_digits=7, verbose_name="Защита от огня?"
    )
