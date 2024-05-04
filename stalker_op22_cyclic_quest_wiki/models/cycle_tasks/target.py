from django.db import models
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel

from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import CyclicQuest


class CycleTaskTargetManager(PolymorphicManager):
    def get_by_natural_key(self, quest_game_code: str) -> "CycleTaskTarget":
        quest = CyclicQuest.objects.get_by_natural_key(quest_game_code)
        return self.get(quest=quest)


class CycleTaskTarget(PolymorphicModel):
    class Meta:
        verbose_name_plural = "Цели ЦЗ"
        verbose_name = "Цель ЦЗ"
    objects = CycleTaskTargetManager()
    quest = models.ForeignKey(
        "CyclicQuest",
        null=False,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name="ЦЗ",
        related_name="target",
    )

    def natural_key(self) -> tuple:
        return (self.quest_id,)


class CycleTaskTargetItem(CycleTaskTarget):
    class Meta:
        verbose_name = "Предмет - цель ЦЗ"
        verbose_name_plural = "Предметы - цели ЦЗ"

    item = models.ForeignKey(
        "Item",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Целевой предмет",
        related_name="quests_when_needed",
    )

    count = models.PositiveIntegerField(
        null=True, verbose_name="Кол-во нужных предметов"
    )
    cond_str = models.CharField(
        max_length=255, null=True, verbose_name="Цель: состояние предмета "
    )

    def __str__(self):
        return f"{self.count or 1} {self.item} {self.cond_str or ''} для {self.quest}"


class CycleTaskTargetCamp(CycleTaskTarget):
    class Meta:
        verbose_name = "Лагерь - цель ЦЗ"
        verbose_name_plural = "Лагеря - цели ЦЗ"

    map_position = models.ForeignKey(
        "MapPosition",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Место на карте",
        related_name="camps_in_position",
    )
    communities = models.ManyToManyField("Community", verbose_name="Группы в лагере", related_name="+")

    def __str__(self):

        communities = (
            ", ".join(str(community) for community in self.communities.all())
            if not self._state.adding
            else ""
        )
        return f"Лагерь {self.map_position} {communities} для {self.quest}"


class CycleTaskTargetStalker(CycleTaskTarget):
    class Meta:
        verbose_name = "Сталкер цель ЦЗ"
        verbose_name_plural = "Сталкеры цель ЦЗ"

    rank = models.ForeignKey(
        "StalkerRank",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Ранг сталкера",
        related_name="+",
    )
    community = models.ForeignKey(
        "Community",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="группа сталкера",
        related_name="+",
    )
    map_positions = models.ManyToManyField(
        "MapPosition",
        verbose_name="Возможные места спавна",
        related_name="+",
    )

    def __str__(self):
        return f"Сталкер {self.rank}, {self.community} для {self.quest}"


__all__ = [
    "CycleTaskTarget",
    "CycleTaskTargetCamp",
    "CycleTaskTargetItem",
    "CycleTaskTargetStalker",
]
