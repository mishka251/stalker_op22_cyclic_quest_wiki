from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from game_parser.models import StorylineCharacter


class GameStoryId(models.Model):

    story_id = models.PositiveSmallIntegerField(
        null=False,
        verbose_name="id в игре",
        unique=True,
    )
    section_name = models.CharField(
        null=False,
        max_length=255,
        verbose_name="Название секции",
        unique=True,
    )

    item = models.ForeignKey(
        null=True,
        to="BaseItem",
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Предмет",
    )
    treasure = models.ForeignKey(
        null=True,
        to="Treasure",
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Тайник",
    )
    character = models.ForeignKey(
        null=True,
        to="StorylineCharacter",
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Предмет",
    )
    spawn_section = models.ForeignKey(
        null=True,
        to="SpawnItem",
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Секция спавна",
    )
    spawn_section_custom = models.ForeignKey(
        null=True,
        to="CustomSpawnItem",
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Кастоная секция спавна",
    )

    class Meta:
        verbose_name = "Связь id с секциями"
        verbose_name_plural = "Связи id с секциями"

    def __str__(self) -> str:
        return f"{self.story_id}"

    def get_stalker_profile(self) -> "StorylineCharacter | None":
        character = None
        if self.spawn_section:
            character = character or self.spawn_section.character_profile
        if self.spawn_section_custom:
            character = character or self.spawn_section_custom.character_profile
        return character or self.character
