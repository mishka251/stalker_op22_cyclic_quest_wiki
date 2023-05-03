from django.db import models



class CycleTaskVendor(models.Model):

    game_story_id_raw = models.PositiveSmallIntegerField(null=False, verbose_name='game id')
    vendor_id = models.PositiveSmallIntegerField(null=False, verbose_name='game id')
    game_story_id = models.ForeignKey(null=True, to='GameStoryId', on_delete=models.SET_NULL)
