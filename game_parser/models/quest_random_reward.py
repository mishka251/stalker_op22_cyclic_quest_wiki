from django.db import models


class QuestRandomReward(models.Model):
    index = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="Индекс",
        unique=True,
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Игровое название",
        unique=True,
    )
    caption = models.CharField(
        max_length=255,
        verbose_name="Человекочитабельное название(из комментария)",
        null=True,
    )
    possible_items_str = models.CharField(
        max_length=2_000,
        verbose_name="Названия возможных предметов",
    )
    possible_items = models.ManyToManyField(
        "game_parser.BaseItem",
        verbose_name="Возможные предметы",
    )

    name_translation = models.ForeignKey(
        "Translation",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Перевод названия",
        related_name="+",
    )
    icon = models.ForeignKey(
        "Icon",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Иконка",
        related_name="+",
    )

    class Meta:
        verbose_name = "Случайная награда за квест"
        verbose_name_plural = "Случайные награды за квесты"

    def __str__(self) -> str:
        if self.name_translation:
            return self.name_translation.rus
        if self.caption:
            return self.caption
        return self.name
