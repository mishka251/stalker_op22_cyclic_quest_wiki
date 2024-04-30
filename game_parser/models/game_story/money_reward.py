from django.db import models

from game_parser.models.game_story.base_script_reward import BaseScriptReward


class MoneyReward(BaseScriptReward):
    class Meta:
        ...
    count = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    raw_count = models.CharField(max_length=512, null=False)

    def __str__(self):
        count = self.count or self.raw_count
        return f"{count} руб."
