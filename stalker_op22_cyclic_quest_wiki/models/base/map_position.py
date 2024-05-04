from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from stalker_op22_cyclic_quest_wiki.models import CycleTaskTargetCamp


class MapPositionManager(models.Manager["MapPosition"]):
    def get_by_natural_key(self, spawn_id: str) -> "MapPosition":
        return self.get(spawn_id=spawn_id)


class MapPosition(models.Model):
    class Meta:
        verbose_name = "Точка на локации"
        verbose_name_plural = "Точки на локации"

    camps_in_position: "RelatedManager[CycleTaskTargetCamp]"
    objects = MapPositionManager()

    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        unique=False,
        null=False,
    )
    x = models.FloatField(null=False)
    y = models.FloatField(null=False)
    z = models.FloatField(null=False)
    spawn_id = models.PositiveBigIntegerField(verbose_name="ID", unique=True)
    story_id = models.PositiveBigIntegerField(
        verbose_name="story_id",
        unique=True,
        null=True,
    )

    spawn_story_id = models.PositiveBigIntegerField(
        verbose_name="spawn_story_id",
        unique=True,
        null=True,
    )
    game_vertex_id = models.PositiveBigIntegerField(verbose_name="vertexID")

    location = models.ForeignKey(
        "Location",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name="Локация",
    )

    def __str__(self):
        return f"{self.name} - {self.x}, {self.y}, {self.z} на локации {self.location}"

    def natural_key(self) -> tuple:
        return (self.spawn_id,)


__all__ = [
    "MapPosition",
]
