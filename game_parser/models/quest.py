from django.db import models

from game_parser.models.character import Character
from game_parser.models.items.base_item import BaseItem


class QuestKinds(models.TextChoices):
    eliminate_lager = ('eliminate_lager',  'Уничтожить лагерь')
    chain = 'chain', 'Цепочка'
    kill_stalker = 'kill_stalker', 'Убить сталкера'
    monster_part = 'monster_part', 'Часть мутанта'
    artefact = 'artefact', 'Принести артефакт'
    find_item = 'find_item', 'Принести предмет'
    defend_lager = 'defend_lager', 'Защитить лагерь'


class CyclicQuest(models.Model):
    class Meta:
        verbose_name = 'Циклический квест'
        verbose_name_plural = 'Циклические квесты'

    type = models.CharField(choices=QuestKinds.choices, null=False, max_length=255, verbose_name='Тип задания(тип цели задания)')
    game_code = models.CharField(null=False, max_length=255, verbose_name='Игровой код в файле')
    giver_code_local = models.CharField(null=True, max_length=255, verbose_name='Код квестодателя(локальный)')
    giver_code_global = models.CharField(null=True, max_length=255, verbose_name='Код квестодателя(глобальный)')
    reward_item_string = models.TextField(null=True, verbose_name='Награда. Предметы(-ы)')
    reward_info_string = models.CharField(null=True, max_length=255, verbose_name='Награда. Информация')
    random_rewards_string = models.CharField(null=True, max_length=255, verbose_name='Награда. Случайная')
    prior = models.IntegerField(default=0,null=False, verbose_name=' Типа очередность задания')
    target_str = models.CharField(null=True, max_length=255, verbose_name='Цель задания')

    # giver = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, max_length=255, verbose_name='Персонаж квестодатель')

    once = models.BooleanField(default=False, verbose_name='Одноразовый ли квест')
    condlist_str = models.CharField(max_length=1_000, null=True, verbose_name='Условия для возможности получения задания')
    target_count = models.PositiveIntegerField(null=True, verbose_name='Кол-во нужных предметов')
    reward_money = models.PositiveIntegerField(null=True, verbose_name='Награда. Деньги')
    map_location = models.CharField(max_length=255, null=True, verbose_name='Цель: на карте')
    target_cond_str = models.CharField(max_length=255, null=True, verbose_name='Цель: состояние премдмета ')
    hide_reward = models.BooleanField(default=False, verbose_name='Скрытая ли награда')
    reward_treasure = models.BooleanField(default=False, verbose_name='Награда. Тайник')
    reward_dialog_str = models.CharField(max_length=512, null=True, verbose_name='Награда. Диалог(?)')
    defend_target_str = models.CharField(max_length=255, null=True, verbose_name='Цель. Защита(?)')
    reward_relation_str = models.CharField(max_length=255, null=True, verbose_name='Награда. Репутация/отношения')

    target_item = models.ForeignKey(BaseItem, null=True, on_delete=models.SET_NULL, verbose_name='Целевой предмет', related_name='quests_when_needed')
    # reward_items = models.ManyToManyField(BaseItem, related_name='quests_when_giving')
    vendor = models.ForeignKey('CycleTaskVendor', null=True, on_delete=models.SET_NULL, verbose_name='Персонаж квестодатель')
    # random_rewards = models.ManyToManyField('QuestRandomReward', verbose_name='Рандомные награды', related_name='quests', through='QuestRandomRewardThrough')

    target_stalker = models.ForeignKey("SpawnItem", on_delete=models.SET_NULL, null=True, verbose_name="Сталкер цель", related_name="+")
    target_camp_to_destroy = models.ForeignKey("SpawnItem", on_delete=models.SET_NULL, null=True, verbose_name="Лагерь нужно уничтожить", related_name="+")
    target_camp_to_defeat = models.ForeignKey("SpawnItem", on_delete=models.SET_NULL, null=True, verbose_name="Лагерь нужно защитить", related_name="+")

    @property
    def get_vendor_character(self):
        vendor = self.vendor
        game_id = vendor.game_story_id if vendor else None
        character = game_id.character if game_id else None
        return character

    def __str__(self):
        kind_caption = dict(QuestKinds.choices)[self.type]
        target = self.target_item or self.target_str
        return f'{kind_caption} {target} для {self.get_vendor_character}'


class CyclicQuestItemReward(models.Model):
    class Meta:
        unique_together = [
            ('item', 'quest'),
            ('raw_item', 'quest'),
        ]
        verbose_name = 'Предмет в награду за ЦЗ'
        verbose_name_plural = 'Предметы в наградах за ЦЗ'

    item = models.ForeignKey(BaseItem, null=True, on_delete=models.SET_NULL, verbose_name='Целевой предмет', related_name='cyclic_quests_when_needed')
    raw_item = models.CharField(max_length=255, null=False)
    quest = models.ForeignKey(CyclicQuest, null=False, on_delete=models.CASCADE, verbose_name='Предмет', related_name='item_rewards')
    count = models.IntegerField(default=1, null=False)


class QuestRandomRewardThrough(models.Model):
    class Meta:
        verbose_name_plural = 'Связи Цз и случайной награды'
        verbose_name = 'Рандомная награда в ЦЗ'
        unique_together = [
            ('reward', 'quest'),
        ]

    quest = models.ForeignKey(CyclicQuest, on_delete=models.CASCADE, null=False, verbose_name='ЦЗ', related_name='random_rewards')
    reward = models.ForeignKey('QuestRandomReward', on_delete=models.CASCADE, null=False, verbose_name='Тип награды', related_name='quests')
    count = models.IntegerField(default=1, null=False, verbose_name='Кол-во')
