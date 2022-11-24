from django.db import models


class GameObject(models.Model):
    class Meta:
        abstract = True

    game_id = models.CharField(max_length=255, null=False, blank=False)
    caption = models.CharField(max_length=1000, null=False, blank=False)
