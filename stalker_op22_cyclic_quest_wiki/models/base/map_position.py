from django.db import models


class MapPosition(models.Model):
    class Meta:
        verbose_name = "Точка на локации"
        verbose_name_plural = "Точки на локации"
    name = models.CharField(max_length=255, verbose_name="Название", unique=True, null=False)
    x = models.FloatField(null=False)
    y = models.FloatField(null=False)
    z = models.FloatField(null=False)
    spawn_id = models.PositiveBigIntegerField(verbose_name="ID", unique=True)
    story_id = models.PositiveBigIntegerField(verbose_name="story_id", unique=True, null=True)

    spawn_story_id = models.PositiveBigIntegerField(verbose_name="spawn_story_id", unique=True, null=True)
    game_vertex_id = models.PositiveBigIntegerField(verbose_name="vertexID")

    location = models.ForeignKey("Location", on_delete=models.SET_NULL, null=True, blank=True)
