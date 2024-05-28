import dataclasses
from typing import TYPE_CHECKING

from django.urls import reverse

from stalker_op22_cyclic_quest_wiki.models import (
    Item,
    ItemReward,
    QuestRandomReward,
    RandomRewardInfo,
)
from stalker_op22_cyclic_quest_wiki.services.base.icon import IconData
from stalker_op22_cyclic_quest_wiki.services.base.translation import TranslationData

if TYPE_CHECKING:
    from django.db.models import QuerySet


@dataclasses.dataclass
class CyclicQuestVendorInfo:
    name: TranslationData
    code: str
    quests_url: str
    icon: IconData

    def to_json(self) -> dict:
        return {
            "name": self.name.to_json(),
            "code": self.code,
            "quests_url": self.quests_url,
            "icon": self.icon.to_json(),
        }


@dataclasses.dataclass
class TargetInQuestInfo:
    vendor: CyclicQuestVendorInfo
    prior: int
    caption: str
    count: int

    def to_json(self) -> dict:
        return {
            "vendor": self.vendor.to_json(),
            "prior": self.prior,
            "caption": self.caption,
            "count": self.count,
        }


@dataclasses.dataclass
class RandomRewardData:
    icon: IconData
    caption: TranslationData
    cyclic_quests: list[TargetInQuestInfo]

    def to_json(self) -> dict:
        return {
            "icon": self.icon.to_json(),
            "caption": self.caption.to_json(),
            "cyclic_quests": [quest.to_json() for quest in self.cyclic_quests],
        }


@dataclasses.dataclass
class ItemUsageInfo:
    icon: IconData
    name: str
    caption: TranslationData
    cyclic_quests: list[TargetInQuestInfo]
    random_reward: list[RandomRewardData]

    def to_json(self) -> dict:
        return {
            "icon": self.icon.to_json(),
            "name": self.name,
            "caption": self.caption.to_json(),
            "cyclic_quests": [quest.to_json() for quest in self.cyclic_quests],
            "random_reward": [quest.to_json() for quest in self.random_reward],
        }


def get_item_usages(item: Item) -> ItemUsageInfo:
    reward_in_quests: QuerySet[ItemReward] = item.use_in_quest_rewards.all()
    random_reward_in_quests: QuerySet[RandomRewardInfo] = (
        item.randomrewardinfo_set.all()
    )
    cyclic_quests_info = [
        _quest_to_dict(quest_reward) for quest_reward in reward_in_quests
    ]
    random_rewards_info = [
        _random_reward_to_dict(random_reward)
        for random_reward in random_reward_in_quests
    ]
    icon_info = IconData.from_icon(item.icon)
    return ItemUsageInfo(
        icon_info,
        item.name,
        TranslationData.from_translation(item.name_translation),
        cyclic_quests_info,
        random_rewards_info,
    )


def _random_reward_to_dict(random_reward: RandomRewardInfo) -> RandomRewardData:
    cyclic_quests_info = [
        _random_reward_quest_to_dict(quest_reward)
        for quest_reward in random_reward.use_in_quests.all()
    ]
    return RandomRewardData(
        IconData.from_icon(random_reward.icon),
        TranslationData.from_translation(random_reward.description),
        cyclic_quests_info,
    )


def _random_reward_quest_to_dict(quest_target: QuestRandomReward) -> TargetInQuestInfo:
    vendor = quest_target.quest.vendor
    vendor_icon = IconData.from_icon(vendor.icon)
    vendor_info = CyclicQuestVendorInfo(
        name=TranslationData.from_translation(vendor.name_translation),
        code=vendor.section_name,
        quests_url=reverse("vendor_tasks", args=(vendor.id,)),
        icon=vendor_icon,
    )
    return TargetInQuestInfo(
        vendor_info,
        quest_target.quest.prior,
        str(quest_target.quest),
        count=quest_target.count or 1,
    )


def _quest_to_dict(quest_target: ItemReward) -> TargetInQuestInfo:
    vendor = quest_target.quest.vendor
    vendor_icon = IconData.from_icon(vendor.icon)
    vendor_info = CyclicQuestVendorInfo(
        name=TranslationData.from_translation(vendor.name_translation),
        code=vendor.section_name,
        quests_url=reverse("vendor_tasks", args=(vendor.id,)),
        icon=vendor_icon,
    )
    return TargetInQuestInfo(
        vendor_info,
        quest_target.quest.prior,
        str(quest_target.quest),
        count=quest_target.count or 1,
    )
