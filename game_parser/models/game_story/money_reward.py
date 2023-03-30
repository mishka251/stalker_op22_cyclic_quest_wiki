from game_parser.models import BaseItem
from game_parser.models.game_story.base_script_reward import BaseScriptReward
from django.db import models

class MoneyReward(BaseScriptReward):
    class Meta:
        ...
    count = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    raw_count = models.CharField(max_length=512, null=False)

