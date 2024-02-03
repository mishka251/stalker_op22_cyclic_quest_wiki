from django.db import models

class Monster(models.Model):
    class Meta:
        verbose_name = "Мутант"
        verbose_name_plural = "Мутанты"

    section_name = models.CharField(max_length=255, null=False)
    short_name = models.CharField(max_length=255, null=True)

    visual_str = models.CharField(max_length=255, null=True)
    corpse_visual_str = models.CharField(max_length=255, null=True)
    icon_str = models.CharField(max_length=255, null=True)

    Spawn_Inventory_Item_Section = models.CharField(max_length=255, null=True)
    Spawn_Inventory_Item_Probability = models.CharField(max_length=255, null=True)
    class_name = models.CharField(max_length=255, null=True)
    terrain = models.CharField(max_length=255, null=True)
    species = models.CharField(max_length=255, null=True)
    spec_rank = models.CharField(max_length=255, null=True)

    icon = models.ForeignKey("Icon", on_delete=models.SET_NULL, null=True)
    monster_part = models.ForeignKey("MonsterPart", on_delete=models.SET_NULL, null=True)
    name_translation = models.ForeignKey("Translation", on_delete=models.SET_NULL, null=True)
