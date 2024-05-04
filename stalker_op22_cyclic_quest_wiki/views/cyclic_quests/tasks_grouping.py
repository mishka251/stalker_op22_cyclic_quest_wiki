import dataclasses
import re
from itertools import groupby
from typing import NamedTuple, Optional

from stalker_op22_cyclic_quest_wiki.models import (
    Ammo,
    CycleTaskTargetCamp,
    CycleTaskTargetItem,
    CycleTaskTargetStalker,
    CycleTaskVendor,
    CyclicQuest,
    ItemReward,
    MapPosition,
    MoneyReward,
    QuestRandomReward,
)
from stalker_op22_cyclic_quest_wiki.models import TreasureReward as TreasureRewardModel
from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import QuestKinds

position_re = re.compile(r"\s*(?P<x>.*),\s*(?P<y>.*),\s*(?P<z>.*)")
offset_re = re.compile(
    r"\s*(?P<min_x>.*),\s*(?P<min_y>.*),\s*(?P<max_x>.*),\s*(?P<max_y>.*)",
)


@dataclasses.dataclass
class Icon:
    url: str
    width: int
    height: int


@dataclasses.dataclass
class ItemInfo:
    item_id: str
    item_label: str
    icon: Icon | None


@dataclasses.dataclass
class MapPointItem:
    position: tuple[float, float]
    info_str: str


@dataclasses.dataclass
class MapPointInfo:
    unique_map_id: str
    image_url: str
    bounds: tuple[float, float, float, float]
    item: MapPointItem
    y_level_offset: float


@dataclasses.dataclass
class QuestTarget:
    pass


@dataclasses.dataclass
class QuestItemTarget(QuestTarget):
    item: ItemInfo
    items_count: int


class ItemState(NamedTuple):
    min: float
    max: float


@dataclasses.dataclass
class QuestItemWithStateTarget(QuestItemTarget):
    state: ItemState


@dataclasses.dataclass
class AmmoTarget(QuestItemTarget):
    ammo_count: int


@dataclasses.dataclass
class LagerTarget(QuestTarget):
    map_info: MapPointInfo | None = None


@dataclasses.dataclass
class StalkerTarget(QuestTarget):
    stalker_str: str
    possible_points: list[MapPointInfo]
    rank: str
    community: str


@dataclasses.dataclass
class TaskReward:
    pass


@dataclasses.dataclass
class TaskMoneyReward(TaskReward):
    count: int


@dataclasses.dataclass
class TaskItemReward(TaskReward):
    item: ItemInfo
    items_count: int


@dataclasses.dataclass
class TreasureReward(TaskReward):
    pass


@dataclasses.dataclass
class TaskRandomReward(TaskReward):
    count: int
    reward_name: str
    icon: Icon | None


@dataclasses.dataclass
class TaskAmmoReward(TaskItemReward):
    ammo_count: int


@dataclasses.dataclass
class Quest:
    target: QuestTarget
    rewards: list[TaskReward]
    text: str | None


QuestGroupByPriority = dict[int, list[Quest]]


@dataclasses.dataclass
class CharacterQuests:
    character_id: int
    character_name: str
    quest_group_by_type: dict[QuestKinds, QuestGroupByPriority]


def collect_vendor_tasks(
    _vendor_tasks: list[CyclicQuest],
    vendor: CycleTaskVendor,
) -> CharacterQuests:
    vendor_tasks = list(sorted(_vendor_tasks, key=lambda task: task.type))
    vendor_id = vendor.game_story_id

    vendor_name = vendor.name_translation.rus
    quest_group_by_type = {}
    for _task_kind, _vendor_kind_tasks in groupby(
        vendor_tasks,
        key=lambda task: task.type,
    ):
        task_kind = QuestKinds[_task_kind]
        vendor_kind_tasks = list(
            sorted(_vendor_kind_tasks, key=lambda task: task.prior),
        )
        tasks_by_prior = {}
        for prior, _prior_tasks in groupby(
            vendor_kind_tasks,
            key=lambda task: task.prior,
        ):
            prior_tasks = list(_prior_tasks)

            prior_quests = [parse_task(task) for task in prior_tasks]
            tasks_by_prior[prior] = prior_quests
        quest_group_by_type[task_kind] = tasks_by_prior
    return CharacterQuests(vendor_id, vendor_name, quest_group_by_type)


def parse_task(db_task: CyclicQuest) -> Quest:
    target = parse_target(db_task)
    rewards = [
        parse_item_reward(reward) for reward in ItemReward.objects.filter(quest=db_task)
    ]
    if (reward_money := MoneyReward.objects.filter(quest=db_task).first()) is not None:
        rewards.append(TaskMoneyReward(reward_money.money))

    if TreasureRewardModel.objects.filter(quest=db_task).exists():
        rewards.append(TreasureReward())

    for random_reward in QuestRandomReward.objects.filter(quest=db_task):
        icon_ = random_reward.reward.icon.icon
        icon = Icon(icon_.url, icon_.width, icon_.height)
        reward = TaskRandomReward(
            count=random_reward.count,
            reward_name=random_reward.reward.description.rus,
            icon=icon,
        )
        rewards.append(reward)

    return Quest(target, rewards, db_task.text.rus if db_task.text else None)


def parse_target(db_task: CyclicQuest) -> QuestTarget:
    items_types = {
        QuestKinds.chain,
        QuestKinds.monster_part,
        QuestKinds.artefact,
        QuestKinds.find_item,
    }

    lager_types = {
        QuestKinds.eliminate_lager,
        QuestKinds.defend_lager,
    }

    stalker_types = {QuestKinds.kill_stalker}

    if db_task.type in stalker_types:
        stalker = CycleTaskTargetStalker.objects.get(quest=db_task)
        possible_spawn_items = stalker.map_positions.all()
        maybe_map_points = [
            _spawn_item_to_map_info(item, f"{db_task.game_code}_stalker_{i}")
            for i, item in enumerate(possible_spawn_items)
        ]
        return StalkerTarget(
            str(stalker),
            [point for point in maybe_map_points if point is not None],
            stalker.rank.translation.rus,
            stalker.community.translation.rus,
        )
    if db_task.type in lager_types:
        target_camp = CycleTaskTargetCamp.objects.get(quest=db_task)
        camp_map_info = _spawn_item_to_map_info(
            target_camp.map_position,
            f"{db_task.game_code}_target_camp",
        )
        return LagerTarget(camp_map_info)

    if db_task.type in items_types:
        target = CycleTaskTargetItem.objects.get(quest=db_task)
        target_item = target.item.get_real_instance()
        target_cond_str: str | None = target.cond_str
        item_icon = None
        if target_item.icon:
            item_icon = Icon(
                target_item.icon.icon.url,
                target_item.icon.icon.width,
                target_item.icon.icon.height,
            )

        item_info = ItemInfo(
            item_id=target_item.name,
            item_label=(
                target_item.name_translation.rus
                if target_item.name_translation
                else target_item.inv_name
            ),
            icon=item_icon,
        )
        target_count = target.count or 1

        if target_cond_str:
            if "," in target_cond_str:
                min_str, max_str = target_cond_str.split(",")
                state = ItemState(float(min_str.strip()), float(max_str.strip()))
            else:
                state = ItemState(float(target_cond_str.strip()), 100)
            return QuestItemWithStateTarget(
                item=item_info,
                items_count=target_count,
                state=state,
            )

        if isinstance(target_item, Ammo):

            return AmmoTarget(
                item=item_info,
                items_count=target_count,
                ammo_count=target_count * target_item.box_size,
            )
        return QuestItemTarget(
            item=item_info,
            items_count=target_count,
        )

    raise NotImplementedError


def _spawn_item_to_map_info(
    target_camp: MapPosition,
    unique_map_id: str,
) -> MapPointInfo | None:
    map_info = target_camp.location.map_info
    if map_info:
        return MapPointInfo(
            unique_map_id,
            image_url=map_info.map_image.url,
            bounds=(map_info.min_x, map_info.min_y, map_info.max_x, map_info.max_y),
            y_level_offset=-(map_info.max_y + map_info.min_y),
            item=MapPointItem(
                position=(target_camp.x, target_camp.z),
                info_str=str(target_camp.spawn_id),
            ),
        )
    return None


def parse_item_reward(reward: ItemReward) -> TaskReward:
    item_icon = None
    if reward.item.icon:
        item_icon = Icon(
            reward.item.icon.icon.url,
            reward.item.icon.icon.width,
            reward.item.icon.icon.height,
        )
    item_info = ItemInfo(
        item_id=reward.item.name,
        item_label=(
            reward.item.name_translation.rus
            if reward.item.name_translation
            else reward.item.inv_name
        ),
        icon=item_icon,
    )
    if isinstance(reward.item, Ammo):
        return TaskAmmoReward(
            item=item_info,
            items_count=reward.count,
            ammo_count=reward.count * reward.item.box_size,
        )
    return TaskItemReward(
        item=item_info,
        items_count=reward.count,
    )
