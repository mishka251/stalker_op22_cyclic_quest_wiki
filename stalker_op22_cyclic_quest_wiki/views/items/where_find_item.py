import dataclasses
from typing import TYPE_CHECKING, Any

from django.urls import reverse
from django.views.generic import TemplateView

from stalker_op22_cyclic_quest_wiki.models import Item, ItemReward

if TYPE_CHECKING:
    from django.db.models import QuerySet


@dataclasses.dataclass
class IconData:
    url: str
    width: int
    height: int


@dataclasses.dataclass
class CyclicQuestVendorInfo:
    name: str
    code: str
    quests_url: str
    icon: IconData


@dataclasses.dataclass
class TargetInQuestInfo:
    vendor: CyclicQuestVendorInfo
    prior: int
    caption: str
    count: int


@dataclasses.dataclass
class ItemUsageInfo:
    icon: IconData
    name: str
    caption: str
    cyclic_quests: list[TargetInQuestInfo]


def get_item_usages(item: Item) -> ItemUsageInfo:
    reward_in_quests: QuerySet[ItemReward] = item.use_in_quest_rewards.all()
    cyclic_quests_info = [
        _quest_to_dict(quest_reward) for quest_reward in reward_in_quests
    ]
    icon_info = IconData(
        item.icon.icon.url,
        item.icon.icon.width,
        item.icon.icon.height,
    )
    return ItemUsageInfo(
        icon_info,
        item.name,
        item.name_translation.rus,
        cyclic_quests_info,
    )


def _quest_to_dict(quest_target: ItemReward) -> TargetInQuestInfo:
    vendor = quest_target.quest.vendor
    vendor_icon = IconData(
        vendor.icon.icon.url,
        vendor.icon.icon.width,
        vendor.icon.icon.height,
    )
    vendor_info = CyclicQuestVendorInfo(
        name=vendor.name_translation.rus,
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


class WhereFindItemView(TemplateView):
    template_name = "wiki/items/where_find.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        item_id = kwargs["item_id"]
        item = Item.objects.get(id=item_id)
        data = get_item_usages(item)
        base_context = super().get_context_data(**kwargs)
        return {
            **base_context,
            "where_find_info": data,
        }
