from django.db import models


class GameStoryId(models.Model):

    story_id = models.PositiveSmallIntegerField(null=False, verbose_name='game id')
    section_name = models.CharField(null=False, max_length=255, verbose_name='Название секции')

    item = models.ForeignKey(null=True, to='BaseItem', on_delete=models.SET_NULL)
    treasure = models.ForeignKey(null=True, to='Treasure', on_delete=models.SET_NULL)
    character = models.ForeignKey(null=True, to='StorylineCharacter', on_delete=models.SET_NULL)
    spawn_section = models.ForeignKey(null=True, to="SpawnItem", on_delete=models.SET_NULL)
    spawn_section_custom = models.ForeignKey(null=True, to="CustomSpawnItem", on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.story_id}'

    def get_stalker_profile(self) -> "Optional[StorylineCharacter]":
        character = None
        if self.spawn_section:
            character = character or self.spawn_section.character_profile
        if self.spawn_section_custom:
            character = character or self.spawn_section_custom.character_profile
        character = character or self.character
        return character
