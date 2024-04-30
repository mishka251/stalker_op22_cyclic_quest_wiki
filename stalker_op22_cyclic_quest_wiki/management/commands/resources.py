import dataclasses

from django.db.models import Model
from import_export.resources import ModelResource

from stalker_op22_cyclic_quest_wiki.models import Translation, Icon, Community, StalkerRank, Location, LocationMapInfo, \
    Item, Ammo, MapPosition, CyclicQuest, ItemReward, MoneyReward, QuestRandomReward, RandomRewardInfo, TreasureReward, \
    CycleTaskVendor, CycleTaskTargetCamp, CycleTaskTargetItem, CycleTaskTargetStalker
from stalker_op22_cyclic_quest_wiki.resources import TranslationResource, IconResource, CommunityResource, \
    StalkerRankResource, LocationResource, LocationMapInfoResource, ItemResource, AmmoResource, MapPositionResource, \
    CyclicQuestResource, ItemRewardResource, MoneyRewardResource, QuestRandomRewardResource, RandomRewardInfoResource, \
    TreasureRewardResource, CycleTaskVendorResource, CycleTaskTargetCampResource, CycleTaskTargetItemResource, \
    CycleTaskTargetStalkerResource


@dataclasses.dataclass
class ModelToExport:
    model_cls: type[Model]
    resource_cls: type[ModelResource]
    file_name: str


to_export: list[ModelToExport] = [
    ModelToExport(Translation, TranslationResource, "translations.csv"),
    ModelToExport(Icon, IconResource, "icons.csv"),
    ModelToExport(Community, CommunityResource, "communities.csv"),
    ModelToExport(StalkerRank, StalkerRankResource, "ranks.csv"),
    ModelToExport(LocationMapInfo, LocationMapInfoResource, "location_maps.csv"),
    ModelToExport(Location, LocationResource, "locations.csv"),
    ModelToExport(Item, ItemResource, "items.csv"),
    ModelToExport(Ammo, AmmoResource, "ammo.csv"),
    ModelToExport(MapPosition, MapPositionResource, "map_points.csv"),

    ModelToExport(CycleTaskVendor, CycleTaskVendorResource, "vendors.csv"),
    ModelToExport(CyclicQuest, CyclicQuestResource, "quests.csv"),
    ModelToExport(ItemReward, ItemRewardResource, "item_rewards.csv"),
    ModelToExport(MoneyReward, MoneyRewardResource, "money_rewards.csv"),
    ModelToExport(RandomRewardInfo, RandomRewardInfoResource, "random_rewards.csv"),
    ModelToExport(QuestRandomReward, QuestRandomRewardResource, "quest_random_rewards.csv"),
    ModelToExport(TreasureReward, TreasureRewardResource, "treasure_rewards.csv"),
    ModelToExport(CycleTaskTargetCamp, CycleTaskTargetCampResource, "target_camps.csv"),
    ModelToExport(CycleTaskTargetItem, CycleTaskTargetItemResource, "target_items.csv"),
    ModelToExport(CycleTaskTargetStalker, CycleTaskTargetStalkerResource, "target_stalkers.csv"),
]
