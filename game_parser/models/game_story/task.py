from django.db import models

from game_parser.models import Translation
from game_parser.models.game_story.storyline_character import Icon


class GameTask(models.Model):
    game_id = models.CharField(max_length=256, unique=True)
    title_id_raw = models.CharField(max_length=256)
    title = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL)
    prio = models.IntegerField(null=True)


class TaskObjective(models.Model):
    task = models.ForeignKey(GameTask, on_delete=models.CASCADE)
    text_id_raw = models.CharField(max_length=256, null=True)
    text = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL, related_name='+')

    icon_raw = models.CharField(max_length=512, null=True)
    icon = models.ForeignKey(Icon, null=True, on_delete=models.SET_NULL, related_name='+')

    article_id_raw = models.CharField(max_length=256, null=True)
    article = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL, related_name='+')

    function_complete_raw = models.TextField(null=True)
    infoportion_complete_raw = models.TextField(null=True)
    infoportion_set_complete_raw = models.TextField(null=True)
    object_story_id_raw = models.TextField(null=True)
    function_fail_raw = models.TextField(null=True)
    infoportion_set_fail_raw = models.TextField(null=True)
    function_call_complete_raw = models.TextField(null=True)
    # infoportion_set_fail_raw = models.TextField(null=True)

class MapLocationType(models.Model):
    objective = models.ForeignKey(TaskObjective, on_delete=models.CASCADE)
    hint_raw = models.CharField(max_length=256, null=True)
    hint = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL, related_name='+')
    location_type = models.CharField(max_length=256)
