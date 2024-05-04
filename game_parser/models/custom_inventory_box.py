from django.db import models


class InventoryBox(models.Model):
    """
    Похоже, это тайник в виде рюкзака, из которого можно достать предметы
    """

    class Meta:
        verbose_name = "Тайник"
        verbose_name_plural = "Тайники"

    section_name = models.CharField(
        max_length=255,
        verbose_name="Название секции",
        unique=True,
    )
    source_file_name = models.CharField(
        max_length=255,
        verbose_name="Путь к файлу(custom_data)",
    )
    items_raw = models.CharField(
        max_length=1000,
        verbose_name="Строка с предметами",
        null=True,
    )
    visual_str = models.CharField(
        max_length=255,
        verbose_name="Внешний вид(название - visual)",
        null=True,
    )

    def __str__(self):
        return f"Тайник {self.section_name}"


class ItemInTreasureBox(models.Model):
    class Meta:
        verbose_name = "Предметы в тайнике"
        verbose_name_plural = "Предметы в тайниках"
        unique_together = [
            ["item", "box"],
        ]

    item = models.ForeignKey(
        "BaseItem",
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Предмет",
    )
    box = models.ForeignKey(
        "InventoryBox",
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Тайник",
    )
    count = models.IntegerField(null=True, verbose_name="Количество")

    def __str__(self):
        return f"{self.count} {self.item} в {self.box}"
