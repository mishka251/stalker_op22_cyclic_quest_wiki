from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import ItemReward, MoneyReward, QuestRandomReward, RandomRewardInfo, TreasureReward


@register(ItemReward)
class ItemRewardAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
        "item",
    ]
    search_fields = [
        "quest__code",
        "item__name",
    ]


@register(MoneyReward)
class MoneyRewardAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
    ]


@register(QuestRandomReward)
class QuestRandomRewardAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
        "reward",
    ]


@register(RandomRewardInfo)
class RandomRewardInfoAdmin(ModelAdmin):
    autocomplete_fields = [
        "description",
        "icon",
        "possible_items",
    ]

    search_fields = [
        "index",
        "description__rus",
    ]


@register(TreasureReward)
class TreasureRewardAdmin(ModelAdmin):
    autocomplete_fields = [
        "quest",
    ]

