import dataclasses
from typing import TYPE_CHECKING

from django.urls import reverse

from stalker_op22_cyclic_quest_wiki.models import CycleTaskTargetItem, Item
from stalker_op22_cyclic_quest_wiki.services.base.condition import ItemCondition
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
            "name": self.name,
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
    condition: ItemCondition | None

    def to_json(self) -> dict:
        return {
            "vendor": self.vendor.to_json(),
            "prior": self.prior,
            "caption": self.caption,
            "count": self.count,
            "condition": self.condition.to_json() if self.condition else None,
        }


@dataclasses.dataclass
class ItemUsageInfo:
    icon: IconData
    name: str
    caption: TranslationData
    cyclic_quests: list[TargetInQuestInfo]

    def to_json(self) -> dict:
        return {
            "icon": self.icon.to_json(),
            "name": self.name,
            "caption": self.caption,
            "cyclic_quests": [quest.to_json() for quest in self.cyclic_quests],
        }


def get_item_usages(item: Item) -> ItemUsageInfo:
    reward_in_quests: QuerySet[CycleTaskTargetItem] = item.quests_when_needed.all()
    cyclic_quests_info = [
        _quest_to_dict(quest_reward) for quest_reward in reward_in_quests
    ]
    icon_info = IconData.from_icon(
        item.icon,
    )
    return ItemUsageInfo(
        icon_info,
        item.name,
        TranslationData.from_translation(item.name_translation),
        cyclic_quests_info,
    )


def _quest_to_dict(quest_target: CycleTaskTargetItem) -> TargetInQuestInfo:
    vendor = quest_target.quest.vendor
    vendor_icon = IconData.from_icon(
        vendor.icon,
    )
    vendor_info = CyclicQuestVendorInfo(
        name=TranslationData.from_translation(vendor.name_translation),
        code=vendor.section_name,
        quests_url=reverse("vendor_tasks", args=(vendor.id,)),
        icon=vendor_icon,
    )
    condition = None
    target_cond_str = quest_target.cond_str
    if target_cond_str:
        if "," in target_cond_str:
            min_str, max_str = target_cond_str.split(",")
            condition = ItemCondition(float(min_str.strip()), float(max_str.strip()))
        else:
            condition = ItemCondition(float(target_cond_str.strip()), 100)
    return TargetInQuestInfo(
        vendor_info,
        quest_target.quest.prior,
        str(quest_target.quest),
        count=quest_target.count or 1,
        condition=condition,
    )
