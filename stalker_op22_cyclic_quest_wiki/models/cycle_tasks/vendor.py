from django.db import models

from stalker_op22_cyclic_quest_wiki.models.base.icon import Icon
from stalker_op22_cyclic_quest_wiki.models.base.map_position import MapPosition
from stalker_op22_cyclic_quest_wiki.models.base.translation import Translation


class CyclicQuestManager(models.Manager["CycleTaskVendor"]):
    def get_by_natural_key(self, local_id: int) -> "CycleTaskVendor":
        return self.get(local_id=local_id)


class CycleTaskVendor(models.Model):

    section_name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
        verbose_name="Название секции НПС",
    )
    local_id = models.PositiveIntegerField(
        null=False,
        verbose_name="ID квестодателя локальный(в cycle_task.ltx)",
        unique=True,
    )
    game_story_id = models.PositiveIntegerField(
        null=False,
        verbose_name="ID квестодателя глобальный(story_id)",
        unique=True,
    )
    name_translation = models.ForeignKey(
        Translation,
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Имя НПС",
        related_name="+",
    )
    icon = models.ForeignKey(
        Icon,
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Фото НПС",
        related_name="+",
    )
    position = models.ForeignKey(
        MapPosition,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Где обитает",
        related_name="+",
    )
    objects = CyclicQuestManager()

    class Meta:
        verbose_name = "Квестодатель"
        verbose_name_plural = "Квестодатели"

    def __str__(self) -> str:
        return self.name_translation.rus or self.name_translation.code

    def natural_key(self) -> tuple:
        return (self.local_id,)


__all__ = [
    "CycleTaskVendor",
]
