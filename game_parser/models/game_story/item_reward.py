from game_parser.models import BaseItem
from game_parser.models.game_story.base_script_reward import BaseScriptReward
from django.db import models

class ItemReward(BaseScriptReward):
    class Meta:
        ...
    item = models.ForeignKey(BaseItem, verbose_name='Предмет', null=True, on_delete=models.SET_NULL)
    raw_item = models.CharField(max_length=512, null=False)
    count = models.IntegerField(null=True)
    raw_count = models.CharField(max_length=512, null=False)