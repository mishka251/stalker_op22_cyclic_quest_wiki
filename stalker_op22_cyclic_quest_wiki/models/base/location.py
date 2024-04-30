from django.db import models


class LocationManager(models.Manager):
    def get_by_natural_key(self, name: str) -> "Location":
        return self.get(name=name)

class Location(models.Model):
    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
    objects = LocationManager()
    name = models.CharField(max_length=255, unique=True, null=False)
    name_translation = models.ForeignKey("Translation", null=True, verbose_name="Перевод названия",
                                         on_delete=models.SET_NULL)
    map_info = models.ForeignKey("LocationMapInfo", null=True, on_delete=models.PROTECT, verbose_name="Карта локации")

    def natural_key(self) -> tuple:
        return (self.name, )

    def __str__(self):
        return self.name_translation.rus


class LocationMapInfoManager(models.Manager):
    def get_by_natural_key(self, location_name: str) -> "LocationMapInfo":
        return self.get(location_name=location_name)


class LocationMapInfo(models.Model):
    class Meta:
        verbose_name = "Карта локации"
        verbose_name_plural = "Карты локации"
    objects = LocationMapInfoManager()
    location_name = models.CharField(max_length=255, unique=True, null=False)
    map_image = models.ImageField(null=False, verbose_name="Карта")
    min_x = models.FloatField(null=False)
    max_x = models.FloatField(null=False)
    min_y = models.FloatField(null=False)
    max_y = models.FloatField(null=False)

    def natural_key(self) -> tuple:
        return (self.location_name, )

    def __str__(self):
        return f"Карта {self.location_set.first()}"

__all__ = [
    "Location",
    "LocationMapInfo",
]
