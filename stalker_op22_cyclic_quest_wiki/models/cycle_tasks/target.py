from django.db import models
from polymorphic.models import PolymorphicModel


class CycleTaskTarget(PolymorphicModel):
    class Meta:
        verbose_name_plural = "Цели ЦЗ"
        verbose_name = "Цель ЦЗ"

    quest = models.ForeignKey("CyclicQuest", null=False, on_delete=models.CASCADE, unique=True, verbose_name="ЦЗ")

    def natural_key(self) -> tuple:
        return (self.quest_id, )


class CycleTaskTargetItem(CycleTaskTarget):
    class Meta:
        verbose_name = 'Предмет - цель ЦЗ'
        verbose_name_plural = 'Предметы - цели ЦЗ'
    item = models.ForeignKey("Item", null=True, on_delete=models.SET_NULL, verbose_name='Целевой предмет',
                                    related_name='quests_when_needed')

    count = models.PositiveIntegerField(null=True, verbose_name='Кол-во нужных предметов')
    cond_str = models.CharField(max_length=255, null=True, verbose_name='Цель: состояние предмета ')


class CycleTaskTargetCamp(CycleTaskTarget):
    class Meta:
        verbose_name = 'Лагерь - цель ЦЗ'
        verbose_name_plural = 'Лагеря - цели ЦЗ'
    map_position = models.ForeignKey("MapPosition", null=False, on_delete=models.PROTECT, verbose_name="Место на карте")
    communities = models.ManyToManyField("Community", verbose_name="Группы в лагере")


class CycleTaskTargetStalker(CycleTaskTarget):
    class Meta:
        verbose_name = "Сталкер цель ЦЗ"
        verbose_name_plural = "Сталкеры цель ЦЗ"
    # stalker = models.ForeignKey("StalkerSection", on_delete=models.SET_NULL, null=True,
    #                                    verbose_name="Сталкер цель", )
    rank = models.ForeignKey("StalkerRank", null=False, on_delete=models.PROTECT, verbose_name="Ранг сталкера")
    community = models.ForeignKey("Community", null=False, on_delete=models.PROTECT, verbose_name="группа сталкера")
    map_positions = models.ManyToManyField("MapPosition", verbose_name="Возможные места спавна")




