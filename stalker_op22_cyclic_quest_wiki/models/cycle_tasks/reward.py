from typing import TYPE_CHECKING

from django.db import models

from stalker_op22_cyclic_quest_wiki.models.base.base_item import Item
from stalker_op22_cyclic_quest_wiki.models.base.icon import Icon
from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import CyclicQuest

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class MoneyRewardManager(models.Manager["MoneyReward"]):

    def get_by_natural_key(self, quest_game_code: str) -> "MoneyReward":
        quest = CyclicQuest.objects.get_by_natural_key(quest_game_code)
        return self.get(quest=quest)


class MoneyReward(models.Model):
    class Meta:
        unique_together = [
            ("quest"),
        ]
        verbose_name = "Деньги за ЦЗ"
        verbose_name_plural = "Деньги за ЦЗ"

    objects = MoneyRewardManager()
    money = models.PositiveIntegerField(null=False, verbose_name="Сумма")

    quest = models.ForeignKey(
        "CyclicQuest",
        null=False,
        on_delete=models.CASCADE,
        verbose_name="ЦЗ",
    )

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(),)

    def __str__(self):
        return f"{self.money} рублей за квест {self.quest}"


class ItemRewardManager(models.Manager["ItemReward"]):

    def get_by_natural_key(self, quest_game_code: str, item_name: str) -> "ItemReward":
        quest = CyclicQuest.objects.get_by_natural_key(quest_game_code)
        item = Item.objects.get_by_natural_key(item_name)
        return self.get(quest=quest, item=item)


class ItemReward(models.Model):
    class Meta:
        unique_together = [
            ("item", "quest"),
        ]
        verbose_name = "Предмет за ЦЗ"
        verbose_name_plural = "Предметы за ЦЗ"

    objects = ItemRewardManager()
    item = models.ForeignKey(
        "Item",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Предмет",
        related_name="use_in_quest_rewards",
    )
    count = models.PositiveIntegerField(
        default=1,
        null=False,
        verbose_name="Кол-во предметов",
    )

    quest = models.ForeignKey(
        "CyclicQuest",
        null=False,
        on_delete=models.CASCADE,
        verbose_name="ЦЗ",
    )

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(), *self.item.natural_key())

    def __str__(self):
        return f"{self.count} {self.item} за квест {self.quest}"


class QuestRandomRewardManager(models.Manager["QuestRandomReward"]):

    def get_by_natural_key(
        self,
        quest_game_code: str,
        reward_index: int,
    ) -> "QuestRandomReward":
        quest = CyclicQuest.objects.get_by_natural_key(quest_game_code)
        reward = RandomRewardInfo.objects.get_by_natural_key(reward_index)
        return self.get(quest=quest, reward=reward)


class QuestRandomReward(models.Model):
    class Meta:
        unique_together = [
            ("reward", "quest"),
        ]
        verbose_name = "Случайная награда за ЦЗ"
        verbose_name_plural = "Случайная награда за ЦЗ"

    objects = QuestRandomRewardManager()
    reward = models.ForeignKey(
        "RandomRewardInfo",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Описание случайной награды",
        related_name="use_in_quests",
    )
    count = models.PositiveIntegerField(
        default=1,
        null=False,
        verbose_name="Количество",
    )

    quest = models.ForeignKey(
        "CyclicQuest",
        null=False,
        on_delete=models.CASCADE,
        verbose_name="ЦЗ",
    )

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(), *self.reward.natural_key())

    def __str__(self):
        return f"{self.count} {self.reward} за квест {self.quest}"


class RandomRewardInfoManager(models.Manager["RandomRewardInfo"]):
    def get_by_natural_key(self, index: int) -> "RandomRewardInfo":
        return self.get(index=index)


class RandomRewardInfo(models.Model):
    class Meta:
        verbose_name = "Описание случайной награды"
        verbose_name_plural = "Описание случайных наград"

    objects = RandomRewardInfoManager()
    use_in_quests: "RelatedManager[QuestRandomReward]"
    index = models.IntegerField(null=False, unique=True, verbose_name="Индекс")
    icon = models.ForeignKey(
        Icon,
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Иконка",
        related_name="+",
    )
    description = models.ForeignKey(
        "Translation",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Описание",
        related_name="+",
    )
    possible_items = models.ManyToManyField("Item", verbose_name="Возможные предметы")

    def natural_key(self) -> tuple:
        return (self.index,)

    def __str__(self):
        return self.description.rus or self.description.code


class TreasureRewardManager(models.Manager["TreasureReward"]):

    def get_by_natural_key(self, quest_game_code: str) -> "TreasureReward":
        quest = CyclicQuest.objects.get_by_natural_key(quest_game_code)
        return self.get(quest=quest)


class TreasureReward(models.Model):
    class Meta:
        unique_together = [
            ("quest",),
        ]
        verbose_name = "Тайник в награду за ЦЗ"
        verbose_name_plural = "Тайники в награду за ЦЗ"

    objects = TreasureRewardManager()

    quest = models.ForeignKey(
        "CyclicQuest",
        null=False,
        on_delete=models.CASCADE,
        verbose_name="ЦЗ",
    )

    def natural_key(self) -> tuple:
        return (*self.quest.natural_key(),)

    def __str__(self):
        return f"Тайник за квест {self.quest}"


__all__ = [
    "ItemReward",
    "MoneyReward",
    "QuestRandomReward",
    "RandomRewardInfo",
    "TreasureReward",
]
