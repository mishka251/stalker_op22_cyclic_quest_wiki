from typing import Optional, TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from game_parser.models import StorylineCharacter, SpawnItem


class CycleTaskVendor(models.Model):
    class Meta:
        verbose_name = "ID НПС, выдающий циклические задания"
        verbose_name_plural = "ID Выдающих ЦЗ НПС"

    game_story_id_raw = models.PositiveSmallIntegerField(null=False, verbose_name='game id', unique=True)
    vendor_id = models.PositiveSmallIntegerField(null=False, verbose_name='game id', unique=True)
    game_story_id = models.ForeignKey(null=True, to='GameStoryId', on_delete=models.SET_NULL, unique=True)

    def __str__(self):
        return f"{self.game_story_id}, {self.vendor_id}"

    def get_spawn_section(self) -> "Optional[SpawnItem]":
        game_story_id = self.game_story_id
        if not game_story_id:
            return None
        spawn_section = game_story_id.spawn_section
        return spawn_section

    def _get_game_story_character_profile(self)-> "Optional[StorylineCharacter]":
        game_story_id = self.game_story_id
        if not game_story_id:
            return None
        return game_story_id.get_stalker_profile()

    def _get_spawn_section_npc_profile(self) -> "Optional[StorylineCharacter]":
        spawn_section = self.get_spawn_section()
        if not spawn_section:
            return None
        return spawn_section.character_profile

    def get_npc_profile(self) -> "Optional[StorylineCharacter]":
        return self._get_spawn_section_npc_profile() or self._get_game_story_character_profile()
