from typing import TYPE_CHECKING

from django.db import models

from stalker_op22_cyclic_quest_wiki.models.base.location import Location

if TYPE_CHECKING:
    from stalker_op22_cyclic_quest_wiki.models import CycleTaskTargetCamp


class MapPositionManager(models.Manager["MapPosition"]):
    def get_by_natural_key(
        self,
        name: str,
    ) -> "MapPosition":
        return self.get(name=name)


class MapPosition(models.Model):
    camps_in_position: "models.Manager[CycleTaskTargetCamp]"
    x = models.FloatField(null=False)
    y = models.FloatField(null=False)
    z = models.FloatField(null=False)
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        unique=False,
        null=False,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name="Локация",
    )
    objects = MapPositionManager()

    class Meta:
        verbose_name = "Точка на локации"
        verbose_name_plural = "Точки на локации"
        unique_together = [
            ("x", "y", "z", "location"),
        ]
        indexes = [
            models.Index(fields=("x", "y", "z", "location"), name="map_position_index"),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.x}, {self.y}, {self.z} на локации {self.location}"

    def natural_key(self) -> tuple:
        return (self.name,)


__all__ = [
    "MapPosition",
]
