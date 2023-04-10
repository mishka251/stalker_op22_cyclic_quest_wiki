from game_parser.models import Character, Translation
from django.db import models

class Community(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=512, null=True)


class Icon(models.Model):
    name = models.CharField(max_length=512, null=False)
    icon = models.ImageField(null=False)

    def __str__(self):
        return f'{self.name}'


class StorylineCharacter(Character):
    game_id = models.CharField(max_length=256)
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
    money_min_raw=models.CharField(max_length=12, null=True)
    money_max_raw=models.CharField(max_length=12, null=True)
    money_inf_raw=models.CharField(max_length=12, null=True)

    terrain_sect_raw = models.TextField(null=True)
    bio_raw = models.TextField(null=True)
    team_raw = models.TextField(null=True)

    NPC_RANDOM_NAME = 'GENERATE_NAME_stalker'

    @property
    def get_name(self) -> str:
        if self.name_translation:
            return self.name_translation.rus
        if self.name_raw == StorylineCharacter.NPC_RANDOM_NAME:
            return 'Случайное имя'
        return self.name_raw
