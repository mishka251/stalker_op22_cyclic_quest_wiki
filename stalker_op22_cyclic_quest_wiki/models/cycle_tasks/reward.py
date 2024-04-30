from django.db import models
from polymorphic.models import PolymorphicModel

from stalker_op22_cyclic_quest_wiki.models.base.icon import Icon


class QuestReward(PolymorphicModel):
    class Meta:
        abstract = True
        verbose_name = "Награда за ЦЗ"
        verbose_name_plural = "Награды за ЦЗ"

    quest = models.ForeignKey("CyclicQuest", null=False, on_delete=models.CASCADE, verbose_name="ЦЗ")


class MoneyReward(QuestReward):
    class Meta:
        unique_together = [
            ("quest"),
        ]
        verbose_name = "Деньги за ЦЗ"
        verbose_name_plural = "Деньги за ЦЗ"

    money = models.PositiveIntegerField(null=False, verbose_name="Сумма")

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(),)

    def __str__(self):
        return f"{self.money} рублей за квест {self.quest}"


class ItemReward(QuestReward):
    class Meta:
        unique_together = [
            ("item", "quest"),
        ]
        verbose_name = "Предмет за ЦЗ"
        verbose_name_plural = "Предметы за ЦЗ"

    item = models.ForeignKey("Item", null=False, on_delete=models.PROTECT, verbose_name="Предмет")
    count = models.PositiveIntegerField(default=1, null=False, verbose_name="Кол-во предметов")

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(), *self.item.natural_key())

    def __str__(self):
        return f"{self.count} {self.item} за квест {self.quest}"

class QuestRandomReward(QuestReward):
    class Meta:
        unique_together = [
            ("reward", "quest"),
        ]
        verbose_name = "Случайная награда за ЦЗ"
        verbose_name_plural = "Случайная награда за ЦЗ"

    reward = models.ForeignKey("RandomRewardInfo", null=False, on_delete=models.PROTECT, verbose_name="Описание случайной награды")
    count = models.PositiveIntegerField(default=1, null=False, verbose_name="Количество")

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(), *self.reward.natural_key())

    def __str__(self):
        return f"{self.count} {self.reward} за квест {self.quest}"


class RandomRewardInfo(models.Model):
    class Meta:
        verbose_name = "Описание случайной награды"
        verbose_name_plural = "Описание случайных наград"
    index = models.IntegerField(null=False, unique=True, verbose_name="Индекс")
    icon = models.ForeignKey(Icon, null=False, on_delete=models.PROTECT, verbose_name="Иконка")
    description = models.ForeignKey("Translation", null=False, on_delete=models.PROTECT, verbose_name="Описание")
    possible_items = models.ManyToManyField("Item", verbose_name="Возможные предметы")

    def natural_key(self) -> tuple:
        return (self.index,)

    def __str__(self):
        return self.description.rus or self.description.code

class TreasureReward(QuestReward):
    class Meta:
        unique_together = [
            ("quest",),
        ]
        verbose_name = "Тайник в награду за ЦЗ"
        verbose_name_plural = "Тайники в награду за ЦЗ"

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(),)

    def __str__(self):
        return f"Тайник за квест {self.quest}"

__all__ = [
    "ItemReward",
    "MoneyReward",
    "QuestRandomReward",
    "QuestReward",
    "RandomRewardInfo",
    "TreasureReward",
]
