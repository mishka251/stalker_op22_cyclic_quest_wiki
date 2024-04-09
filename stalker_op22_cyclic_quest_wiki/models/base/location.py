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
    name_translation = models.ForeignKey("Translation", null=True, verbose_name='Перевод названия',
                                         on_delete=models.SET_NULL)
    offset_str = models.CharField(null=True, max_length=255, verbose_name='Сдвиг на глобальной карте??')

    global_rect_raw = models.CharField(max_length=255, null=True,
                                       verbose_name="Границы локации(относительно глобальной карты?)")
    map_info = models.ForeignKey("LocationMapInfo", null=True, on_delete=models.PROTECT, verbose_name="Карта локации")

    def natural_key(self):
        return (self.name, )

class LocationMapInfo(models.Model):
    class Meta:
        verbose_name = "Карта локации"
        verbose_name_plural = "Карты локации"
    location_name = models.CharField(max_length=255, unique=True, null=False)
    map_image = models.ImageField(null=False, verbose_name="Карта")
    bound_rect_raw = models.CharField(max_length=255, null=False, verbose_name="Границы локации(границы картинки?)")

    min_x = models.FloatField(null=False)
    max_x = models.FloatField(null=False)
    min_y = models.FloatField(null=False)
    max_y = models.FloatField(null=False)

    def natural_key(self):
        return (self.location_name, )

