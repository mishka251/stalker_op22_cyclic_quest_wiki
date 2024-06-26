from typing import TYPE_CHECKING

from django.db import models

from game_parser.models.items.base_item import BaseItem

if TYPE_CHECKING:
    from game_parser.models import StorylineCharacter


class QuestKinds(models.TextChoices):
    DESTROY_CAMP = ("eliminate_lager", "Уничтожить лагерь")
    CHAIN = "chain", "Цепочка"
    KILL = "kill_stalker", "Убить сталкера"
    MONSTER_PART = "monster_part", "Часть мутанта"
    ARTEFACT = "artefact", "Принести артефакт"
    OTHER_ITEM = "find_item", "Принести предмет"
    DEFEND_LAGER = "defend_lager", "Защитить лагерь"


class CyclicQuest(models.Model):

    type = models.CharField(
        choices=QuestKinds.choices,
        null=False,
        max_length=255,
        verbose_name="Тип задания(тип цели задания)",
    )
    game_code = models.CharField(
        null=False,
        max_length=255,
        verbose_name="Игровой код в файле",
        unique=True,
    )
    giver_code_local = models.CharField(
        null=True,
        max_length=255,
        verbose_name="Код квестодателя(локальный)",
    )
    giver_code_global = models.CharField(
        null=True,
        max_length=255,
        verbose_name="Код квестодателя(глобальный)",
    )
    reward_item_string = models.TextField(
        null=True,
        verbose_name="Награда. Предметы(-ы)",
    )
    reward_info_string = models.CharField(
        null=True,
        max_length=255,
        verbose_name="Награда. Информация",
    )
    random_rewards_string = models.CharField(
        null=True,
        max_length=255,
        verbose_name="Награда. Случайная",
    )
    prior = models.IntegerField(
        default=0,
        null=False,
        verbose_name=" Типа очередность задания",
    )
    target_str = models.CharField(
        null=True,
        max_length=255,
        verbose_name="Цель задания",
    )

    once = models.BooleanField(default=False, verbose_name="Одноразовый ли квест")
    condlist_str = models.CharField(
        max_length=1_000,
        null=True,
        verbose_name="Условия для возможности получения задания",
    )
    target_count = models.PositiveIntegerField(
        null=True,
        verbose_name="Кол-во нужных предметов",
    )
    reward_money = models.PositiveIntegerField(
        null=True,
        verbose_name="Награда. Деньги",
    )
    map_location = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Цель: на карте",
    )
    target_cond_str = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Цель: состояние премдмета ",
    )
    hide_reward = models.BooleanField(default=False, verbose_name="Скрытая ли награда")
    reward_treasure = models.BooleanField(default=False, verbose_name="Награда. Тайник")
    reward_dialog_str = models.CharField(
        max_length=512,
        null=True,
        verbose_name="Награда. Диалог(?)",
    )
    defend_target_str = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Цель. Защита(?)",
    )
    reward_relation_str = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Награда. Репутация/отношения",
    )
    target_camp = models.ForeignKey(
        "CampInfo",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Цель - лагерь",
    )
    target_item = models.ForeignKey(
        BaseItem,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Целевой предмет",
        related_name="quests_when_needed",
    )
    vendor = models.ForeignKey(
        "CycleTaskVendor",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Персонаж квестодатель",
    )
    target_camp_to_destroy = models.ForeignKey(
        "SpawnItem",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Лагерь нужно уничтожить",
        related_name="+",
    )
    target_camp_to_defeat = models.ForeignKey(
        "SpawnItem",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Лагерь нужно защитить",
        related_name="+",
    )

    text_raw = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Код перевода текста задания",
    )
    text = models.ForeignKey(
        "Translation",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Текст задания",
        related_name="+",
    )
    target_stalker = models.ForeignKey(
        "StalkerSection",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сталкер цель",
    )

    class Meta:
        verbose_name = "Циклический квест"
        verbose_name_plural = "Циклические квесты"

    def __str__(self) -> str:
        kind_caption = dict(QuestKinds.choices)[self.type]
        target = self.target_item or self.target_str
        if self.target_count:
            target = f"{self.target_count} {target}"
        return f"{kind_caption} {target} для {self.get_vendor_character}"

    @property
    def get_vendor_character(self) -> "StorylineCharacter | None":
        vendor = self.vendor
        return vendor.get_npc_profile() if vendor else None


class CyclicQuestItemReward(models.Model):
    item = models.ForeignKey(
        BaseItem,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Целевой предмет",
        related_name="cyclic_quests_when_needed",
    )
    raw_item = models.CharField(max_length=255, null=False)
    quest = models.ForeignKey(
        CyclicQuest,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Предмет",
        related_name="item_rewards",
    )
    count = models.IntegerField(default=1, null=False)

    class Meta:
        unique_together = [
            ("item", "quest"),
            ("raw_item", "quest"),
        ]
        verbose_name = "Предмет в награду за ЦЗ"
        verbose_name_plural = "Предметы в наградах за ЦЗ"

    def __str__(self) -> str:
        return f"{self.item} x {self.count} за {self.quest}"


class QuestRandomRewardThrough(models.Model):
    quest = models.ForeignKey(
        CyclicQuest,
        on_delete=models.CASCADE,
        null=False,
        verbose_name="ЦЗ",
        related_name="random_rewards",
    )
    reward = models.ForeignKey(
        "QuestRandomReward",
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Тип награды",
        related_name="quests",
    )
    count = models.IntegerField(default=1, null=False, verbose_name="Кол-во")

    class Meta:
        verbose_name_plural = "Связи Цз и случайной награды"
        verbose_name = "Рандомная награда в ЦЗ"
        unique_together = [
            ("reward", "quest"),
        ]

    def __str__(self) -> str:
        return f"Случайная награда {self.reward} x {self.count} за квест {self.quest}"
