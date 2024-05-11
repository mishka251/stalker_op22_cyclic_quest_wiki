from django.db import models


class LocationManager(models.Manager["Location"]):
    def get_by_natural_key(self, name: str) -> "Location":
        return self.get(name=name)


class Location(models.Model):

    name = models.CharField(max_length=255, unique=True, null=False)
    name_translation = models.ForeignKey(
        "Translation",
        null=True,
        verbose_name="Перевод названия",
        on_delete=models.SET_NULL,
        related_name="+",
    )
    map_info = models.ForeignKey(
        "LocationMapInfo",
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Карта локации",
    )

    objects = LocationManager()

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self) -> str:
        return self.name_translation.rus if self.name_translation else self.name

    def natural_key(self) -> tuple:
        return (self.name,)


class LocationMapInfoManager(models.Manager["LocationMapInfo"]):
    def get_by_natural_key(self, location_name: str) -> "LocationMapInfo":
        return self.get(location_name=location_name)


class LocationMapInfo(models.Model):
    location_name = models.CharField(max_length=255, unique=True, null=False)
    map_image = models.ImageField(null=False, verbose_name="Карта")
    min_x = models.FloatField(null=False)
    max_x = models.FloatField(null=False)
    min_y = models.FloatField(null=False)
    max_y = models.FloatField(null=False)

    objects = LocationMapInfoManager()

    class Meta:
        verbose_name = "Карта локации"
        verbose_name_plural = "Карты локации"

    def __str__(self) -> str:
        return f"Карта {self.location_set.first()}"

    def natural_key(self) -> tuple:
        return (self.location_name,)


__all__ = [
    "Location",
    "LocationMapInfo",
]
