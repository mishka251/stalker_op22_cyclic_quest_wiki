from django.db import models

from game_parser.models import Character, Translation


class CommunityType(models.TextChoices):
    MUTANT = ("monster", "Мутант")
    STALKER = ("stalker", "Сталкер")

class Community(models.Model):
    class Meta:
        verbose_name = "Группировка"
        verbose_name_plural = "Группировки"
    index = models.PositiveSmallIntegerField(null=False, verbose_name="ID группировки", unique=False)
    code = models.CharField(max_length=128, null=False, verbose_name="Код в игре")
    type = models.CharField(choices=CommunityType.choices, null=False, max_length=128, verbose_name="Тип")
    translation = models.ForeignKey("Translation", null=True, on_delete=models.SET_NULL, verbose_name="Перевод названия")

    def __str__(self):
        return self.translation.rus if self.translation else self.code

class RankType(models.TextChoices):
    MUTANT = ("monster", "Мутант")
    STALKER = ("stalker", "Сталкер")

class Rank(models.Model):
    class Meta:
        verbose_name = "Ранг сталкера"
        verbose_name_plural = "Ранги сталкеров"
    name = models.CharField(max_length=128, null=False, unique=True, verbose_name="Код")
    type = models.CharField(choices=RankType.choices, null=False, max_length=128, verbose_name="Тип")
    translation = models.ForeignKey("Translation", null=True, on_delete=models.SET_NULL, verbose_name="Название")
    min_score = models.PositiveSmallIntegerField(null=True, verbose_name="Нижний порог ранга")
    max_score = models.PositiveSmallIntegerField(null=True, verbose_name="Верхний порог ранга")

    def __str__(self):
        return self.translation.rus if self.translation else self.name


class Icon(models.Model):
    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"
    name = models.CharField(max_length=512, null=False, unique=True)
    icon = models.ImageField(null=False)

    def __str__(self):
        return f'{self.name}'


class StorylineCharacter(Character):
    game_id = models.CharField(max_length=256, unique=True)
    name_raw = models.CharField(max_length=512)
    name_translation = models.ForeignKey(Translation,null=True,on_delete=models.SET_NULL)

    no_random = models.IntegerField(null=True)

    community_default_raw = models.CharField(max_length=10, null=True,)
    community = models.ForeignKey(Community, null=True, on_delete=models.SET_NULL)

    icon_raw = models.CharField(max_length=512)
    icon = models.ForeignKey(Icon, null=True, on_delete=models.SET_NULL)

    class_raw = models.CharField(max_length=512)

    rank = models.IntegerField(null=True)
    reputation = models.IntegerField(null=True)

    supplies_raw = models.TextField(null=True)
    dialogs_raw = models.TextField(null=True)
    visual_raw = models.TextField(null=True)

    start_dialog_row = models.TextField(null=True)
    comments = models.TextField(null=True)

    crouch_type_raw = models.CharField(max_length=128, null=True)
    snd_config_raw = models.CharField(max_length=128, null=True)
    money_min_raw = models.CharField(max_length=12, null=True)
    money_max_raw = models.CharField(max_length=12, null=True)
    money_inf_raw = models.CharField(max_length=12, null=True)

    terrain_sect_raw = models.TextField(null=True)
    bio_raw = models.TextField(null=True)
    team_raw = models.TextField(null=True)

    dialogs = models.ManyToManyField('Dialog')

    NPC_RANDOM_NAME = 'GENERATE_NAME_stalker'

    @property
    def get_name(self) -> str:
        if self.name_translation:
            return self.name_translation.rus
        if self.name_raw == StorylineCharacter.NPC_RANDOM_NAME:
            return 'Случайное имя'
        return self.name_raw

    def __str__(self):
        return f'NPC {self.get_name}'
