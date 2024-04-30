from django.db import models


class EncyclopediaGroup(models.Model):
    class Meta:
        verbose_name = "Группа в энциклопедии"
        verbose_name_plural = "Группы в энциклопедии"

    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    name_translation = models.ForeignKey("Translation", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.name_translation and self.name_translation.rus:
            return self.name_translation.rus
        return self.name


class EncyclopediaArticle(models.Model):
    class Meta:
        verbose_name = "Статья в энциклопедии"
        verbose_name_plural = "Статьи в энциклопедии"

    game_id = models.CharField(max_length=255, verbose_name="Игровой id", unique=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    name_translation = models.ForeignKey("Translation", null=True, on_delete=models.SET_NULL, related_name="+")
    group_name = models.CharField(max_length=255, verbose_name="Группа", null=True)
    group = models.ForeignKey("EncyclopediaGroup", null=True, on_delete=models.SET_NULL)
    ltx_str = models.CharField(max_length=255, null=True, verbose_name="Иконка", unique=True)
    icon = models.ForeignKey("Icon", null=True, on_delete=models.SET_NULL)
    text = models.TextField(null=False)
    text_translation = models.ForeignKey("Translation", null=True, on_delete=models.SET_NULL, related_name="+")
    artefact = models.ForeignKey("Artefact", null=True, on_delete=models.SET_NULL, related_name="articles")

    def __str__(self) -> str:
        return f"Статья {self.name} в разделе {self.group}"
