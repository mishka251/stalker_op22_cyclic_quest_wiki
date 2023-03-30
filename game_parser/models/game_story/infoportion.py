from django.db import models

from game_parser.models.game_story.task import GameTask


class InfoPortion(models.Model):
    game_id = models.CharField(max_length=512)

    article_raw = models.CharField(max_length=256, null=True)

    disable_raw = models.TextField(null=True)

    task_raw = models.TextField(null=True)
    task = models.ForeignKey(GameTask, null=True, on_delete=models.SET_NULL)

    actions_raw = models.TextField(null=True)

