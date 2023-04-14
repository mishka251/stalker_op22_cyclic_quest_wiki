from django.db import models


class GameStoryId(models.Model):

    story_id = models.PositiveSmallIntegerField(null=False, verbose_name='game id')
    section_name = models.CharField(null=False, max_length=255, verbose_name='Название секции')

    item = models.ForeignKey(null=True, to='BaseItem', on_delete=models.SET_NULL)
    treasure = models.ForeignKey(null=True, to='Treasure', on_delete=models.SET_NULL)
    character = models.ForeignKey(null=True, to='StorylineCharacter', on_delete=models.SET_NULL)

