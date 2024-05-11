from django.db import models

from game_parser.models.items.base_item import BaseItem
from game_parser.models.translation import Translation


class Treasure(models.Model):

    target = models.CharField(
        null=False,
        max_length=10,
        verbose_name="spawn_id для поиска в спавне",
    )
    name_str = models.CharField(
        null=False,
        max_length=255,
        verbose_name="Название(код перевода)",
    )
    description_str = models.CharField(
        null=False,
        max_length=255,
        verbose_name="Описание(код перевода)",
    )
    items_str = models.CharField(
        null=False,
        max_length=1_000,
        verbose_name="Предметы в тайнике(строкой)",
    )
    condlist_str = models.CharField(
        null=False,
        max_length=1_000,
        verbose_name="Условия",
    )
    custom_name = models.CharField(
        null=True,
        max_length=255,
        verbose_name="Название(2)(код перевода)",
    )

    custom_name_translation = models.ForeignKey(
        Translation,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Перевод названия",
        related_name="+",
    )
    description_translation = models.ForeignKey(
        Translation,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Перевод описания",
        related_name="+",
    )

    spawn_item = models.ForeignKey(
        "SpawnItem",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Секция спавна",
        related_name="treasures",
    )

    class Meta:
        verbose_name = "Тайник"
        verbose_name_plural = "Тайники"

    def __str__(self) -> str:
        treasure_str = ""
        if self.custom_name_translation:
            treasure_str += self.custom_name_translation.rus
        treasure_str += f" {self.name_str} {self.target}"
        return treasure_str


class ItemInTreasure(models.Model):
    item = models.ForeignKey(
        BaseItem,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Предмет",
        related_name="has_in_treasures",
    )
    treasure = models.ForeignKey(
        Treasure,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Тайник",
        related_name="items",
    )
    count = models.PositiveIntegerField(verbose_name="Кол-во предметов", default=1)

    class Meta:
        verbose_name = "Предмет в тайнике"
        verbose_name_plural = "Предметы в тайниках"
        unique_together = [
            ["item", "treasure"],
        ]

    def __str__(self) -> str:
        return f"{self.count} {self.item} в {self.treasure}"
