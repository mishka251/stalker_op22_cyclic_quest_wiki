from django.db import models
from polymorphic.models import PolymorphicModel

from game_parser.models.translation import Translation


class BaseItem(PolymorphicModel):
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    visual_str = models.CharField(max_length=255, verbose_name="Название иконки?")
    description_code = models.CharField(
        max_length=255, verbose_name="Код названия(ссылка на переводы)"
    )
    cost = models.PositiveIntegerField(verbose_name="Базовая цена")
    name = models.CharField(
        max_length=255, verbose_name="Название(код в игре)", unique=True
    )

    inv_name = models.CharField(
        max_length=255, verbose_name="Название в инвентаре?", null=True
    )
    inv_name_short = models.CharField(
        max_length=255, verbose_name="Название в инвентаре(сокращенное)?", null=True
    )
    inv_weight = models.DecimalField(
        verbose_name="Вес", decimal_places=3, max_digits=12
    )
    cheat_item = models.BooleanField(default=False)
    quest_item = models.BooleanField(default=False, verbose_name="Квестовый предмет")

    inv_grid_width = models.PositiveIntegerField(
        null=True, verbose_name="Ширина иконки"
    )
    inv_grid_height = models.PositiveIntegerField(
        null=True, verbose_name="Высота иконки"
    )
    inv_grid_x = models.PositiveIntegerField(
        null=True, verbose_name="Отступ по длине иконки в большом файле"
    )
    inv_grid_y = models.PositiveIntegerField(
        null=True, verbose_name="Отступ по высоте иконки в большом файле"
    )

    name_translation = models.ForeignKey(
        Translation,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Перевод названия",
        related_name="+",
    )
    description_translation = models.ForeignKey(
        Translation,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Перевод описания",
        related_name="+",
    )

    inv_icon = models.ImageField(
        null=True, verbose_name="Иконка в инвентаре", upload_to="item_icons/"
    )

    def __str__(self):
        if self.name_translation:
            return self.name_translation.rus
        return self.name
