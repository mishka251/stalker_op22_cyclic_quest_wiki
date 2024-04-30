from django.db import models

from game_parser.models.game_story.base_script_reward import BaseScriptReward
from game_parser.models.items.base_item import BaseItem


class ItemReward(BaseScriptReward):
    class Meta: ...

    item = models.ForeignKey(
        BaseItem,
        verbose_name="Предмет",
        null=True,
        on_delete=models.SET_NULL,
        related_name="got_in_functions",
    )
    raw_item = models.CharField(max_length=512, null=False)
    count = models.IntegerField(null=True)
    raw_count = models.CharField(max_length=512, null=False)

    def __str__(self):
        count = self.count or self.raw_count
        return f"{count} {self.get_item}"

    @property
    def get_item(self) -> str:
        if self.item is not None:
            return str(self.item)
        return self.raw_item
