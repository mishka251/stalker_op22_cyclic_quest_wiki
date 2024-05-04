import dataclasses
import re
from itertools import groupby
from typing import NamedTuple, Optional

from game_parser.models import (
    Ammo,
    LocationMapInfo,
    Outfit,
    Silencer,
    SingleStalkerSpawnItem,
    SpawnItem,
    StorylineCharacter,
    Weapon,
)
from game_parser.models.quest import CyclicQuest, CyclicQuestItemReward, QuestKinds

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
    item_id: str | None
    item_label: str | None
    icon: Icon | None


@dataclasses.dataclass
class MapPointItem:
    position: tuple[float, float]
    info_str: str


@dataclasses.dataclass
class MapPointInfo:
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
    game_id: str
    map_info: MapPointInfo | None = None


@dataclasses.dataclass
class StalkerTarget(QuestTarget):
    game_id: str
    stalker_str: str
    possible_points: list[MapPointInfo]


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
    reward_name: str | None
    reward_id: str
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
    character_id: str
    character_name: str
    quest_group_by_type: dict[QuestKinds, QuestGroupByPriority]


# class CyclicTasksView(TemplateView):


def collect_info() -> list[CharacterQuests]:
    all_tasks = list(CyclicQuest.objects.all().order_by("vendor"))
    result = []
    for vendor, _vendor_tasks in groupby(
        all_tasks,
        lambda task: task.get_vendor_character,
    ):
        result += [collect_vendor_tasks(_vendor_tasks, vendor)]

    return result


def collect_vendor_tasks(_vendor_tasks, vendor: StorylineCharacter) -> CharacterQuests:
    vendor_tasks = list(sorted(_vendor_tasks, key=lambda task: task.type))
    vendor_id = vendor.game_id
    vendor_name = (
        vendor.name_translation.rus
        if vendor.name_translation and vendor.name_translation.rus
        else "<Неизвестный>"
    )
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
    rewards = [parse_item_reward(reward) for reward in db_task.item_rewards.all()]
    if db_task.reward_money is not None:
        rewards.append(TaskMoneyReward(db_task.reward_money))

    if db_task.reward_treasure:
        rewards.append(TreasureReward())

    for random_reward in db_task.random_rewards.all():
        if random_reward.reward is None:
            raise ValueError
        icon = None
        if random_reward.reward.icon and random_reward.reward.icon.icon:
            icon_ = random_reward.reward.icon.icon
            icon = Icon(icon_.url, icon_.width, icon_.height)
        reward = TaskRandomReward(
            count=random_reward.count,
            reward_name=(
                random_reward.reward.name_translation.rus
                if random_reward.reward.name_translation
                else None
            ),
            reward_id=random_reward.reward.name,
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
        stalker = db_task.target_stalker
        if stalker is None:
            raise TypeError
        single_spawn_items = SingleStalkerSpawnItem.objects.filter(
            stalker_section=stalker,
        )
        single_spawn_items_ids = single_spawn_items.values_list(
            "spawn_item_id",
            flat=True,
        )
        respawns = stalker.respawn_set.all()
        respawns_spawn_items = respawns.values_list("spawn_item_id", flat=True)
        possible_spawn_items = SpawnItem.objects.filter(
            id__in=list(single_spawn_items_ids) + list(respawns_spawn_items),
        )
        maybe_map_points = [
            _spawn_item_to_map_info(stalker.section_name, item)
            for item in possible_spawn_items
        ]
        return StalkerTarget(
            str(stalker),
            str(stalker),
            [point for point in maybe_map_points if point is not None],
        )
    if db_task.type in lager_types:
        target_camp = db_task.target_camp  # or db_task.target_camp_to_destroy
        target_camp_item = (
            target_camp.spawn_item
            if target_camp
            else (
                db_task.target_camp_to_destroy
                if db_task.type == QuestKinds.eliminate_lager
                else db_task.target_camp_to_defeat
            )
        )
        if target_camp_item is None:
            raise TypeError
        camp_map_info = _spawn_item_to_map_info(
            target_camp_item.section_name,
            target_camp_item,
        )
        return LagerTarget(db_task.target_str or str(db_task.id), camp_map_info)

    if db_task.type in items_types:
        if db_task.target_item is None:
            raise ValueError
        target_item = db_task.target_item.get_real_instance()
        target_cond_str: str | None = db_task.target_cond_str
        items_with_condition = (Weapon, Outfit, Silencer)
        if target_cond_str is None and isinstance(target_item, items_with_condition):
            target_cond_str = "50"

        item_icon = None
        if target_item.inv_icon:
            item_icon = Icon(
                target_item.inv_icon.url,
                target_item.inv_icon.width,
                target_item.inv_icon.height,
            )

        item_info = ItemInfo(
            item_id=target_item.inv_name,
            item_label=(
                target_item.name_translation.rus
                if target_item.name_translation
                else target_item.inv_name
            ),
            icon=item_icon,
        )
        target_count = db_task.target_count or 1

        if target_cond_str is not None:
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
    target_str: str,
    target_camp: SpawnItem,
) -> MapPointInfo | None:
    if target_camp and target_camp.location:
        location_map_info = LocationMapInfo.objects.filter(
            location=target_camp.location,
        ).first()
        if (
            location_map_info
            and location_map_info.map_image
            and location_map_info.bound_rect_raw
            and (coords_rm := position_re.match(target_camp.position_raw))
        ):
            rm = offset_re.match(location_map_info.bound_rect_raw)
            if rm is None:
                raise ValueError("Err")
            (min_x, min_y, max_x, max_y) = (
                float(rm.group("min_x")),
                float(rm.group("min_y")),
                float(rm.group("max_x")),
                float(rm.group("max_y")),
            )

            (x, _, z) = (
                float(coords_rm.group("x")),
                float(coords_rm.group("y")),
                float(coords_rm.group("z")),
            )
            return MapPointInfo(
                image_url=location_map_info.map_image.url,
                bounds=(min_x, min_y, max_x, max_y),
                y_level_offset=-(max_y + min_y),
                item=MapPointItem(position=(x, z), info_str=target_str),
            )
    return None


def parse_item_reward(reward: CyclicQuestItemReward) -> TaskReward:
    item_icon = None
    if reward.item is None:
        raise ValueError("No item in reward")
    if reward.item.inv_icon:
        item_icon = Icon(
            reward.item.inv_icon.url,
            reward.item.inv_icon.width,
            reward.item.inv_icon.height,
        )
    item_info = ItemInfo(
        item_id=reward.item.inv_name,
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
