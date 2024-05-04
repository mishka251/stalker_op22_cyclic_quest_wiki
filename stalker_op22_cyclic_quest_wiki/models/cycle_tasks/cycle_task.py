from typing import TYPE_CHECKING

from django.db import models

from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.vendor import CycleTaskVendor

if TYPE_CHECKING:
    from polymorphic.managers import PolymorphicManager

    from stalker_op22_cyclic_quest_wiki.models import (
        CycleTaskTarget,
        ItemReward,
        MoneyReward,
        QuestRandomReward,
        TreasureReward,
    )


class QuestKinds(models.TextChoices):
    ELIMINATE_CAMP = ("eliminate_lager", "Уничтожить лагерь")
    CHAIN = "chain", "Цепочка"
    KILL_STALKER = "kill_stalker", "Убить сталкера"
    FIND_MONSTER_PART = "monster_part", "Часть мутанта"
    FIND_ARTEFACT = "artefact", "Принести артефакт"
    FIND_ITEM = "find_item", "Принести предмет"
    DEFEND_CAMP = "defend_lager", "Защитить лагерь"


class CyclicQuestManager(models.Manager["CyclicQuest"]):
    def get_by_natural_key(self, game_code: str) -> "CyclicQuest":
        return self.get(game_code=game_code)


class CyclicQuest(models.Model):
    class Meta:
        verbose_name = "Циклический квест"
        verbose_name_plural = "Циклические квесты"

    itemreward: "models.Manager[ItemReward]"
    moneyreward: "models.Manager[MoneyReward]"
    questrandomreward: "models.Manager[QuestRandomReward]"
    treasurereward: "models.Manager[TreasureReward]"

    target: "PolymorphicManager[CycleTaskTarget]"

    objects = CyclicQuestManager()

    game_code = models.CharField(
        null=False,
        max_length=255,
        verbose_name="Игровой код в файле",
        unique=True,
    )
    type = models.CharField(
        choices=QuestKinds.choices,
        null=False,
        max_length=255,
        verbose_name="Тип задания(тип цели задания)",
    )
    prior = models.IntegerField(
        default=0,
        null=False,
        verbose_name=" Типа очередность задания",
    )
    once = models.BooleanField(default=False, verbose_name="Одноразовый ли квест")

    vendor = models.ForeignKey(
        CycleTaskVendor,
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Кквестодатель",
        related_name="quests",
    )

    text = models.ForeignKey(
        "Translation",
        on_delete=models.PROTECT,
        null=False,
        verbose_name="Текст задания",
        related_name="+",
    )

    def natural_key(self) -> tuple:
        return (self.game_code,)

    def __str__(self):
        type_caption = QuestKinds[self.type].label
        return f"{type_caption}({self.prior}) для {self.vendor}"


__all__ = [
    "CyclicQuest",
]
