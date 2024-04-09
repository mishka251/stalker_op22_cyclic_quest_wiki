from django.db import models


class IconManager(models.Manager):
    def get_by_natural_key(self, name: str) -> "Icon":
        return self.get(name=name)


class Icon(models.Model):
    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"

    objects = IconManager()
    name = models.CharField(max_length=512, null=False, unique=True, verbose_name="Код иконки для связи с объектами")
    icon = models.ImageField(null=False, verbose_name="Иконка")

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return f'{self.name}'
