from django.db import models

from stalker_op22_cyclic_quest_wiki.models.base.icon import Icon
from stalker_op22_cyclic_quest_wiki.models.base.translation import Translation


class CycleTaskVendor(models.Model):
    class Meta:
        verbose_name = "Квестодатель"
        verbose_name_plural = "Квестодатели"
    section_name = models.CharField(max_length=128, null=False, unique=True, verbose_name="Название секции НПС")
    local_id = models.PositiveSmallIntegerField(null=False, verbose_name='ID квестодателя локальный(в cycle_task.ltx)', unique=True)
    game_story_id = models.PositiveSmallIntegerField(null=False, verbose_name='ID квестодателя глобальный(story_id)', unique=True)
    name_translation = models.ForeignKey(Translation, null=False, on_delete=models.PROTECT, verbose_name="Имя НПС")
    icon = models.ForeignKey(Icon, null=False, on_delete=models.PROTECT, verbose_name="Фото НПС")


