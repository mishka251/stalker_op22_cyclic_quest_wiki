from django.db import models


class Translation(models.Model):

    code = models.CharField(
        max_length=128,
        null=False,
        verbose_name="Код названия",
        unique=True,
    )
    rus = models.TextField(verbose_name="Русский", null=False)
    eng = models.TextField(verbose_name="Английский", null=False)
    ukr = models.TextField(verbose_name="Украинский", null=False)
    pln = models.TextField(verbose_name="Польский", null=False)
    fra = models.TextField(verbose_name="Французский", null=False)

    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Переводы"

    def __str__(self) -> str:
        return f"{self.code} {self.rus}"
