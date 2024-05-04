from django.db import models
from polymorphic.models import PolymorphicManager, PolymorphicModel


class ItemManager(PolymorphicManager):
    def get_by_natural_key(self, name: str) -> "Item":
        return self.get(name=name)


class Item(PolymorphicModel):
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    objects = ItemManager()
    cost = models.PositiveIntegerField(verbose_name="Базовая цена")
    name = models.CharField(
        max_length=255,
        verbose_name="Название(код в игре)",
        unique=True,
        null=False,
    )
    inv_weight = models.DecimalField(
        verbose_name="Вес",
        decimal_places=3,
        max_digits=12,
    )
    icon = models.ForeignKey(
        "Icon",
        on_delete=models.PROTECT,
        null=False,
        verbose_name="Иконка",
        related_name="+",
    )
    name_translation = models.ForeignKey(
        "Translation",
        on_delete=models.PROTECT,
        null=False,
        verbose_name="Перевод названия",
        related_name="+",
    )
    description_translation = models.ForeignKey(
        "Translation",
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Перевод описания",
        related_name="+",
    )

    def natural_key(self) -> tuple:
        return (self.name,)

    def __str__(self):
        if self.name_translation:
            return self.name_translation.rus
        return self.name


__all__ = [
    "Item",
]
