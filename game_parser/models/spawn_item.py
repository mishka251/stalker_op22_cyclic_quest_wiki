from django.db import models


class SpawnItem(models.Model):
    class Meta:
        verbose_name = "Секция спавна"
        verbose_name_plural = "Секции спавна"
    section_name = models.CharField(max_length=255, verbose_name="Название секции")
    name = models.CharField(max_length=255, verbose_name="Название")
    position_raw = models.CharField(max_length=300, verbose_name="Координаты(строка)")
    spawn_id = models.PositiveBigIntegerField(verbose_name="ID", unique=True)
    story_id = models.PositiveBigIntegerField(verbose_name="story_id", unique=True, null=True)
    spawn_story_id = models.PositiveBigIntegerField(verbose_name="spawn_story_id", unique=True, null=True)
    game_vertex_id = models.PositiveBigIntegerField(verbose_name="vertexID")
    location_txt = models.CharField(max_length=255, verbose_name="локация")
    custom_data = models.TextField(null=True)

    item = models.ForeignKey("BaseItem", on_delete=models.SET_NULL, null=True, verbose_name="Предмет")
    character_profile_str = models.CharField(max_length=255, verbose_name="Профиль сталкера", null=True)
    character_profile = models.ForeignKey("StorylineCharacter", on_delete=models.SET_NULL, null=True, verbose_name="Профиль НПС")
    npc_logic = models.ForeignKey("NpcLogicConfig", on_delete=models.SET_NULL, null=True, verbose_name="Конфиг логики НПС")

    def __str__(self):
        return f"{self.name} ({self.section_name})"


class NpcLogicConfig(models.Model):
    class Meta:
        verbose_name = "Логики НПС"
        verbose_name_plural = "Файлы логик НПС"

    name = models.CharField(max_length=255, verbose_name="Название файла")
    source_file_name = models.CharField(max_length=255, verbose_name="Исходный файл", null=False, unique=True)
    trade_file_name = models.CharField(max_length=255, verbose_name="Название файла торговли", null=True)
    trade_config = models.ForeignKey("Trader", on_delete=models.SET_NULL, null=True, verbose_name="Конфиг торговли")

    def __str__(self):
        return f"{self.name} ({self.source_file_name})"


class CustomSpawnItem(models.Model):
    section_name = models.CharField(max_length=255, verbose_name="Название секции")
    name = models.CharField(max_length=255, verbose_name="Название")
    custom_data = models.TextField(null=True)

    item = models.ForeignKey("BaseItem", on_delete=models.SET_NULL, null=True, verbose_name="Предмет")
    character_profile_str = models.CharField(max_length=255, verbose_name="Профиль сталкера", null=True)
    character_profile = models.ForeignKey("StorylineCharacter", on_delete=models.SET_NULL, null=True, verbose_name="Профиль НПС")
    npc_logic = models.ForeignKey("NpcLogicConfig", on_delete=models.SET_NULL, null=True, verbose_name="Конфиг логики НПС")

    spec_rank_str = models.CharField(max_length=255, null=True)
    community_str = models.CharField(max_length=255, null=True)
    visual_str = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} ({self.section_name})"
