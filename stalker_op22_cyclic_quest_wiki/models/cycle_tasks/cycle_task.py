from django.db import models

from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.vendor import CycleTaskVendor


class QuestKinds(models.TextChoices):
    eliminate_lager = ("eliminate_lager", "Уничтожить лагерь")
    chain = "chain", "Цепочка"
    kill_stalker = "kill_stalker", "Убить сталкера"
    monster_part = "monster_part", "Часть мутанта"
    artefact = "artefact", "Принести артефакт"
    find_item = "find_item", "Принести предмет"
    defend_lager = "defend_lager", "Защитить лагерь"


class CyclicQuestManager(models.Manager):
    def get_by_natural_key(self, game_code: str) -> "CyclicQuest":
        return self.get(game_code=game_code)


class CyclicQuest(models.Model):
    class Meta:
        verbose_name = "Циклический квест"
        verbose_name_plural = "Циклические квесты"

    objects = CyclicQuestManager()

    game_code = models.CharField(
        null=False, max_length=255, verbose_name="Игровой код в файле", unique=True
    )
    type = models.CharField(
        choices=QuestKinds.choices,
        null=False,
        max_length=255,
        verbose_name="Тип задания(тип цели задания)",
    )
    prior = models.IntegerField(
        default=0, null=False, verbose_name=" Типа очередность задания"
    )
    once = models.BooleanField(default=False, verbose_name="Одноразовый ли квест")

    vendor = models.ForeignKey(
        CycleTaskVendor,
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Кквестодатель",
    )

    text = models.ForeignKey(
        "Translation",
        on_delete=models.PROTECT,
        null=False,
        verbose_name="Текст задания",
        related_name="+",
    )

    def natural_key(self) -> tuple:
        return (self.game_code,)

    def __str__(self):
        type_caption = QuestKinds[self.type].label
        return f"{type_caption}({self.prior}) для {self.vendor}"


__all__ = [
    "CyclicQuest",
]
