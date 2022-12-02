from django.db import models

class Character(models.Model):
    game_code = models.CharField(null=False, max_length=255)
    name = models.CharField(null=True, max_length=255)