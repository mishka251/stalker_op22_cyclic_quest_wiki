from django.db import models


class Anomaly(models.Model):
    section_name = models.CharField(max_length=255, null=False, unique=True)
    class_name = models.CharField(max_length=255, null=False)
    visual_str = models.CharField(max_length=255, null=True)
    hit_type = models.CharField(max_length=255, null=True)
    article = models.ForeignKey(
        "EncyclopediaArticle",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Аномалия"
        verbose_name_plural = "Аномалии"

    def __str__(self) -> str:
        return self.section_name
