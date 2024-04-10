from django.db import models


class Community(models.Model):
    class Meta:
        verbose_name = "Группировка"
        verbose_name_plural = "Группировки"
    name = models.CharField(max_length=128, null=False, unique=True, verbose_name="Код")
    translation = models.ForeignKey("Translation", null=False, on_delete=models.PROTECT, verbose_name="Название")

    def __str__(self):
        return self.translation.rus


class StalkerRank(models.Model):
    class Meta:
        verbose_name = "Ранг сталкера"
        verbose_name_plural = "Ранги сталкеров"
    name = models.CharField(max_length=128, null=False, unique=True, verbose_name="Код")
    translation = models.ForeignKey("Translation", null=False, on_delete=models.PROTECT, verbose_name="Название")

    def __str__(self):
        return self.translation.rus