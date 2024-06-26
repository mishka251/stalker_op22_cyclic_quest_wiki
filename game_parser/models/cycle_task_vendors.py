from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from game_parser.models import SpawnItem, SpawnReward, StorylineCharacter


class CycleTaskVendor(models.Model):
    game_story_id_raw = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="game id",
        unique=True,
    )
    vendor_id = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="game id",
        unique=True,
    )
    game_story_id = models.ForeignKey(
        null=True,
        to="GameStoryId",
        on_delete=models.SET_NULL,
        unique=True,
    )

    class Meta:
        verbose_name = "ID НПС, выдающий циклические задания"
        verbose_name_plural = "ID Выдающих ЦЗ НПС"

    def __str__(self) -> str:
        return f"{self.game_story_id}, {self.vendor_id}"

    def get_spawn_section(self) -> "SpawnItem | None":
        game_story_id = self.game_story_id
        if not game_story_id:
            return None
        return game_story_id.spawn_section

    def _get_game_story_character_profile(self) -> "StorylineCharacter | None":
        game_story_id = self.game_story_id
        if not game_story_id:
            return None
        return game_story_id.get_stalker_profile()

    def _get_spawn_section_npc_profile(self) -> "StorylineCharacter | None":
        spawn_section = self.get_spawn_section()
        if not spawn_section:
            return None
        return spawn_section.character_profile

    def get_npc_profile(self) -> "StorylineCharacter | None":
        return (
            self._get_spawn_section_npc_profile()
            or self._get_game_story_character_profile()
        )

    def get_spawn_item(self) -> "SpawnItem | None":
        return self.get_spawn_section()

    def _get_spawn_rewards_from_game_story_id(self) -> "list[SpawnReward]":
        game_story_id = self.game_story_id
        if not game_story_id:
            return []
        spawn_section_custom = game_story_id.spawn_section_custom
        if not spawn_section_custom:
            return []
        return list(spawn_section_custom.spawn_rewards.all())

    def _get_npc_spawn_rewards(self) -> "list[SpawnReward]":
        npc_profile = self.get_npc_profile()
        if not npc_profile:
            return []
        result = []
        for custom_spawn_item in npc_profile.customspawnitem_set.all():
            result.extend(list(custom_spawn_item.spawn_rewards.all()))
        return result

    def get_spawn_rewards(self) -> "list[SpawnReward]":
        return (
            self._get_spawn_rewards_from_game_story_id() + self._get_npc_spawn_rewards()
        )
