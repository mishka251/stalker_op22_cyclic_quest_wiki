from django.db import models


class IconManager(models.Manager["Icon"]):
    def get_by_natural_key(self, name: str) -> "Icon":
        return self.get(name=name)


class Icon(models.Model):

    name = models.CharField(
        max_length=512,
        null=False,
        unique=True,
        verbose_name="Код иконки для связи с объектами",
    )
    icon = models.ImageField(null=False, verbose_name="Иконка")

    objects = IconManager()

    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"

    def __str__(self):
        return f"{self.name}"

    def natural_key(self) -> tuple:
        return (self.name,)


__all__ = [
    "Icon",
]
