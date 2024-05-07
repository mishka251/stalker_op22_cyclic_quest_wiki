from django.db import models

from game_parser.models.game_story import Community


class SpawnItem(models.Model):
    class Meta:
        verbose_name = "Секция спавна"
        verbose_name_plural = "Секции спавна"

    section_name = models.CharField(max_length=255, verbose_name="Название секции")
    name = models.CharField(max_length=255, verbose_name="Название")
    position_raw = models.CharField(max_length=300, verbose_name="Координаты(строка)")
    spawn_id = models.PositiveBigIntegerField(verbose_name="ID", unique=True)
    story_id = models.PositiveBigIntegerField(
        verbose_name="story_id",
        unique=True,
        null=True,
    )
    spawn_story_id = models.PositiveBigIntegerField(
        verbose_name="spawn_story_id",
        unique=True,
        null=True,
    )
    game_vertex_id = models.PositiveBigIntegerField(verbose_name="vertexID")
    location_txt = models.CharField(max_length=255, verbose_name="локация")
    custom_data = models.TextField(null=True)

    item = models.ForeignKey(
        "BaseItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Предмет",
    )
    character_profile_str = models.CharField(
        max_length=255,
        verbose_name="Профиль сталкера",
        blank=True,
        null=True,
    )
    character_profile = models.ForeignKey(
        "StorylineCharacter",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Профиль НПС",
    )
    npc_logic = models.ForeignKey(
        "NpcLogicConfig",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Конфиг логики НПС",
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="spawn_items",
    )

    def __str__(self):
        return f"{self.name} ({self.section_name})"


class NpcLogicConfig(models.Model):
    class Meta:
        verbose_name = "Логики НПС"
        verbose_name_plural = "Файлы логик НПС"

    name = models.CharField(max_length=255, verbose_name="Название файла")
    source_file_name = models.CharField(
        max_length=255,
        verbose_name="Исходный файл",
        null=False,
        unique=True,
    )
    trade_file_name = models.CharField(
        max_length=255,
        verbose_name="Название файла торговли",
        null=True,
    )
    trade_config = models.ForeignKey(
        "Trader",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Конфиг торговли",
    )

    def __str__(self):
        return f"{self.name} ({self.source_file_name})"


class CustomSpawnItem(models.Model):
    section_name = models.CharField(max_length=255, verbose_name="Название секции")
    name = models.CharField(max_length=255, verbose_name="Название")
    custom_data = models.TextField(null=True)

    item = models.ForeignKey(
        "BaseItem",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Предмет",
    )
    character_profile_str = models.CharField(
        max_length=255,
        verbose_name="Профиль сталкера",
        null=True,
    )
    character_profile = models.ForeignKey(
        "StorylineCharacter",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Профиль НПС",
    )
    npc_logic = models.ForeignKey(
        "NpcLogicConfig",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Конфиг логики НПС",
    )

    spec_rank_str = models.CharField(max_length=255, null=True)
    community_str = models.CharField(max_length=255, null=True)
    visual_str = models.CharField(max_length=255, null=True)
    custom_inventory_box = models.ForeignKey(
        "InventoryBox",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тайник(рюкзак?)",
    )

    def __str__(self):
        return f"{self.name} ({self.section_name})"


class CampInfo(models.Model):
    # для section_name = smart_terrain

    spawn_item = models.ForeignKey(
        "SpawnItem",
        null=False,
        on_delete=models.CASCADE,
        unique=True,
    )
    type = models.CharField(max_length=128, null=True)
    capacity = models.PositiveIntegerField(null=True)
    cond_raw = models.CharField(max_length=512, null=True)
    communities_raw = models.CharField(max_length=512, null=True)
    stay_str = models.CharField(max_length=32, null=True)
    groups_str = models.CharField(max_length=32, null=True)
    communities = models.ManyToManyField(Community)

    class Meta:
        verbose_name_plural = "Лагеря НПС/мутантов"
        verbose_name = "Лагерь НПС/мутантов"

    def __str__(self):
        return f"{self.type}, {self.communities_raw}"


class StalkerSection(models.Model):
    section_name = models.CharField(max_length=255, null=False, unique=True)

    character_profile_str = models.CharField(max_length=128, null=True)
    spec_rank_str = models.CharField(max_length=128, null=True)
    community_str = models.CharField(max_length=128, null=True)
    custom_data_path = models.CharField(max_length=512, null=True)
    community = models.ForeignKey("Community", null=True, on_delete=models.SET_NULL)
    character_profile = models.ForeignKey(
        "StorylineCharacter",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def __str__(self):
        return f"{self.section_name}, {self.character_profile_str} ({self.community_str}, {self.spec_rank_str})"


class Respawn(models.Model):
    # для section_name = respawn

    spawn_item = models.ForeignKey(
        "SpawnItem",
        null=False,
        on_delete=models.CASCADE,
        unique=True,
    )
    respawn_section_raw = models.CharField(max_length=512, null=True)
    max_spawn_raw = models.CharField(max_length=128, null=True)
    idle_spawn_raw = models.CharField(max_length=128, null=True)
    conditions_raw = models.CharField(max_length=128, null=True)

    max_spawn = models.PositiveIntegerField(null=True)
    respawn_section = models.ManyToManyField("game_parser.StalkerSection")

    def __str__(self) -> str:
        return f"Респавн в {self.spawn_item}"


class SingleStalkerSpawnItem(models.Model):
    # для section_name = stalker*

    spawn_item = models.ForeignKey(
        "SpawnItem",
        null=False,
        on_delete=models.CASCADE,
        unique=True,
    )
    character_profile_raw = models.CharField(max_length=512, null=False)
    stalker_section = models.ForeignKey(
        "StalkerSection",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"Спавн сталкера {self.stalker_section}"
