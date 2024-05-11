from django.db import models
from django.db.models import Manager


class TranslationManager(Manager["Translation"]):
    def get_by_natural_key(self, code: str) -> "Translation":
        return self.get(code=code)


class Translation(models.Model):
    code = models.CharField(
        max_length=128,
        null=False,
        verbose_name="Код названия",
        unique=True,
        db_index=True,
    )
    rus = models.TextField(verbose_name="Русский", null=False)
    eng = models.TextField(verbose_name="Английский", null=False)
    ukr = models.TextField(verbose_name="Украинский", null=False)
    pln = models.TextField(verbose_name="Польский", null=False)
    fra = models.TextField(verbose_name="Французский", null=False)

    objects = TranslationManager()

    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Переводы"

    def __str__(self) -> str:
        return f"{self.code} {self.rus}"

    def natural_key(self) -> tuple:
        return (self.code,)


__all__ = [
    "Translation",
]
