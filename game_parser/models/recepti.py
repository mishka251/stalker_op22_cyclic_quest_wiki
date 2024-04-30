from django.db import models


class Recept(models.Model):
    anomaly_id = models.CharField(max_length=255, null=False, unique=True)
    anomaly_name = models.CharField(max_length=255, null=False)
    condition_raw = models.CharField(max_length=255)
    condition = models.ForeignKey(
        "InfoPortion",
        null=True,
        on_delete=models.SET_NULL,
        related_name="opening_recepts",
    )
    components_raw = models.CharField(max_length=255)
    components = models.ManyToManyField("BaseItem", related_name="use_in_recepts")
    cel_raw = models.CharField(max_length=255)
    cel = models.ForeignKey(
        "BaseItem",
        null=True,
        on_delete=models.SET_NULL,
        related_name="cooking_in_recepts",
    )
    v_udachi = models.DecimalField(max_digits=6, decimal_places=3)
    v_virogd = models.DecimalField(max_digits=6, decimal_places=3)
    v_ottorg = models.DecimalField(max_digits=6, decimal_places=3)
    vremya_day = models.CharField(max_length=255)
    vremya_hour = models.CharField(max_length=255)
    vremya_min = models.CharField(max_length=255)
    remove_anomaly = models.BooleanField()
    not_for_mutator = models.BooleanField()
    info_raw = models.CharField(max_length=255, null=True)

    info = models.ForeignKey(
        "InfoPortion",
        null=True,
        on_delete=models.SET_NULL,
        related_name="get_from_recept",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        components = ", ".join(map(str, self.components.all()))
        return f"{self.cel} из {self.anomaly_id}, {self.anomaly_name}. Из {components}"
