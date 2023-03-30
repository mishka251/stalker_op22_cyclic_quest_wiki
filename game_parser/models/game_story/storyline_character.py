from game_parser.models import Character
from django.db import models

class Community(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=512, null=True)

class Icon(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=512, null=True)
    icon = models.ImageField(null=True)

class StorylineCharacter(Character):
    community_default_raw = models.CharField(max_length=10)
    community = models.ForeignKey(Community, null=True, on_delete=models.SET_NULL)
    icon_raw = models.CharField(max_length=512)
    icon = models.ForeignKey(Icon, null=True, on_delete=models.SET_NULL)
    class_raw = models.CharField(max_length=512)

    rank = models.IntegerField(null=True)
    reputation = models.IntegerField(null=True)
    supplies_raw = models.TextField(null=True)
    dialogs_raw = models.TextField(null=True)

