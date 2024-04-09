from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import TreasureReward, RandomRewardInfo, QuestRandomReward, \
    MoneyReward, ItemReward


@register(ItemReward)
class ItemRewardAdmin(ModelAdmin):
    pass


@register(MoneyReward)
class MoneyRewardAdmin(ModelAdmin):
    pass


@register(QuestRandomReward)
class QuestRandomRewardAdmin(ModelAdmin):
    pass


@register(RandomRewardInfo)
class RandomRewardInfoAdmin(ModelAdmin):
    pass


@register(TreasureReward)
class TreasureRewardAdmin(ModelAdmin):
    pass
