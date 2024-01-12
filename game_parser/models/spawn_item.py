from django.db import models

class SpawnItem(models.Model):
    class Meta:
        verbose_name = "Секция спавна"
        verbose_name_plural = "Секции спавна"
    section_name = models.CharField(max_length=255, verbose_name="Название секции")
    name = models.CharField(max_length=255, verbose_name="Название")
    position_raw = models.CharField(max_length=300, verbose_name="Координаты(строка)")
    spawn_id = models.PositiveBigIntegerField(verbose_name="ID", unique=True)
    game_vertex_id = models.PositiveBigIntegerField(verbose_name="vertexID")
    location_txt = models.CharField(max_length=255, verbose_name="локация")
    custom_data = models.TextField(null=True)

    item = models.ForeignKey("BaseItem", on_delete=models.SET_NULL, null=True, verbose_name="Предмет")
    character_profile_str = models.CharField(max_length=255, verbose_name="Профиль сталкера", null=True)

    def __str__(self):
        return f"{self.name} ({self.section_name})"


class NpcLogicConfig(models.Model):
    class Meta:
        verbose_name = "Логики НПС"
        verbose_name_plural = "Файлы логик НПС"

    name = models.CharField(max_length=255, verbose_name="Название файла")
    source_file_name = models.CharField(max_length=255, verbose_name="Исходный файл", null=False, unique=True)
    trade_file_name = models.CharField(max_length=255, verbose_name="Название файла торговли", null=True)
