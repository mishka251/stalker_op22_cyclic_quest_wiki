from django.db import models

class InventoryBox(models.Model):
    section_name = models.CharField(max_length=255)
    source_file_name = models.CharField(max_length=255, verbose_name="Путь к файлу")
    items_raw = models.CharField(max_length=1000, verbose_name="Строка с предметами", null=True)

class ItemInTreasureBox(models.Model):
    item = models.ForeignKey('BaseItem', null=False, on_delete=models.CASCADE)
    box = models.ForeignKey('InventoryBox', null=False, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    