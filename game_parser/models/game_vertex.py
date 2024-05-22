from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from game_parser.models import SpawnReward


class GameVertex(models.Model):
    vertex_id = models.PositiveIntegerField(null=False, unique=True)

    level_point_x = models.FloatField(null=False)
    level_point_y = models.FloatField(null=False)
    level_point_z = models.FloatField(null=False)

    game_point_x = models.FloatField(null=False)
    game_point_y = models.FloatField(null=False)
    game_point_z = models.FloatField(null=False)

    level_id_raw = models.PositiveIntegerField(null=False)
    location = models.ForeignKey("Location", null=True, on_delete=models.SET_NULL)
    level_vertex_id = models.PositiveIntegerField(null=False)
    vertex_type_raw = models.CharField(null=False, max_length=512)
    level_points_raw = models.CharField(null=False, max_length=512)
    edges_raw = models.CharField(null=False, max_length=512)

    class Meta:
        verbose_name = "Узел графа игры"

    spawn_rewards: "models.Manager[SpawnReward]"

    def __str__(self) -> str:
        return f"Вершина {self.vertex_id} на локации {self.level_id_raw}"
