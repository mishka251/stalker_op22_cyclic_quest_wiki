import dataclasses
import re
from functools import lru_cache
from itertools import groupby

from stalker_op22_cyclic_quest_wiki.models import (
    Ammo,
    CycleTaskTarget,
    CycleTaskTargetCamp,
    CycleTaskTargetItem,
    CycleTaskTargetStalker,
    CycleTaskVendor,
    CyclicQuest,
    Icon,
    Item,
    ItemReward,
    MapPosition,
)
from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import QuestKinds
from stalker_op22_cyclic_quest_wiki.utils.condition import ItemCondition

position_re = re.compile(r"\s*(?P<x>.*),\s*(?P<y>.*),\s*(?P<z>.*)")
offset_re = re.compile(
    r"\s*(?P<min_x>.*),\s*(?P<min_y>.*),\s*(?P<max_x>.*),\s*(?P<max_y>.*)",
)


@dataclasses.dataclass
class IconData:
    url: str
    width: int
    height: int

    def to_json(self) -> dict:
        return {
            "url": self.url,
            "width": self.width,
            "height": self.height,
        }


@dataclasses.dataclass
class ItemInfo:
    item_id: str
    item_label: str
    icon: IconData | None

    def to_json(self) -> dict:
        return {
            "item_id": self.item_id,
            "item_label": self.item_label,
            "icon": self.icon.to_json() if self.icon is not None else None,
        }


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

    def to_json(self) -> dict:
        return {
            "image_url": self.image_url,
            "bounds": list(self.bounds),
            "y_level_offset": self.y_level_offset,
            "position": self.item.position,
            "caption": self.item.info_str,
        }


@dataclasses.dataclass
class QuestTarget:
    def to_json(self) -> dict:
        raise NotImplementedError


@dataclasses.dataclass
class QuestItemTarget(QuestTarget):
    item: ItemInfo
    items_count: int

    def to_json(self) -> dict:
        return {
            "_type": "item",
            "item": self.item.to_json(),
            "items_count": self.items_count,
            "state": None,
        }


@dataclasses.dataclass
class QuestItemWithStateTarget(QuestItemTarget):
    state: ItemCondition

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "state": self.state.to_json(),
        }


@dataclasses.dataclass
class AmmoTarget(QuestItemTarget):
    ammo_count: int

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "_type": "ammo",
            "ammo_count": self.ammo_count,
        }


@dataclasses.dataclass
class LagerTarget(QuestTarget):
    map_info: MapPointInfo | None = None

    def to_json(self) -> dict:
        return {
            "_type": "camp",
            "position": self.map_info.to_json() if self.map_info is not None else None,
        }


@dataclasses.dataclass
class StalkerTarget(QuestTarget):
    stalker_str: str
    possible_points: list[MapPointInfo]
    rank: str
    community: str

    def to_json(self) -> dict:
        return {
            "_type": "stalker",
            "stalker_str": self.stalker_str,
            "rank": self.rank,
            "community": self.community,
            "possible_points": [point.to_json() for point in self.possible_points],
        }


@dataclasses.dataclass
class TaskReward:
    def to_json(self) -> dict:
        raise NotImplementedError


@lru_cache
def get_money_icon() -> IconData | None:
    try:
        icon = Icon.objects.get(name="icon_for_item_money_loot")
        return IconData(icon.icon.url, icon.icon.width, icon.icon.height)
    except Icon.DoesNotExist:
        return None


@lru_cache
def get_treasure_icon() -> IconData | None:
    try:
        icon = Icon.objects.get(name="icon_for_item_treasure_item")
        return IconData(icon.icon.url, icon.icon.width, icon.icon.height)
    except Icon.DoesNotExist:
        return None


@dataclasses.dataclass
class TaskMoneyReward(TaskReward):
    count: int

    @property
    def icon(self) -> IconData | None:
        return get_money_icon()

    def to_json(self) -> dict:
        return {
            "_type": "money",
            "count": self.count,
            "icon": self.icon.to_json() if self.icon is not None else None,
        }


@dataclasses.dataclass
class TaskItemReward(TaskReward):
    item: ItemInfo
    items_count: int

    def to_json(self) -> dict:
        return {
            "_type": "item",
            "count": self.items_count,
            "item": self.item.to_json(),
        }


@dataclasses.dataclass
class TreasureReward(TaskReward):
    reward_name = "Тайник"

    @property
    def icon(self) -> IconData | None:
        return get_treasure_icon()

    def to_json(self) -> dict:
        return {
            "_type": "treasure",
            "icon": self.icon.to_json() if self.icon else None,
        }


@dataclasses.dataclass
class TaskRandomReward(TaskReward):
    count: int
    reward_name: str
    icon: IconData | None

    def to_json(self) -> dict:
        return {
            "_type": "random",
            "count": self.count,
            "reward_name": self.reward_name,
            "icon": self.icon.to_json() if self.icon else None,
        }


@dataclasses.dataclass
class TaskAmmoReward(TaskItemReward):
    ammo_count: int

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "_type": "ammo",
            "ammo_count": self.ammo_count,
        }


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
    targets_cache = create_targets_cache(vendor_tasks)

    for _task_kind, _vendor_kind_tasks in groupby(
        vendor_tasks,
        key=lambda task: task.type,
    ):
        task_kind = QuestKinds.get_by_value(_task_kind)
        vendor_kind_tasks = list(
            sorted(_vendor_kind_tasks, key=lambda task: task.prior),
        )
        tasks_by_prior = {}
        for prior, _prior_tasks in groupby(
            vendor_kind_tasks,
            key=lambda task: task.prior,
        ):
            prior_tasks = list(_prior_tasks)

            prior_quests = [parse_task(task, targets_cache) for task in prior_tasks]
            tasks_by_prior[prior] = prior_quests
        quest_group_by_type[task_kind] = tasks_by_prior
    return CharacterQuests(vendor_id, vendor_name, quest_group_by_type)


def create_targets_cache(vendor_tasks: list[CyclicQuest]) -> dict[int, CycleTaskTarget]:
    stalker_targets_cache = {
        target.quest_id: target
        for target in CycleTaskTargetStalker.objects.filter(quest__in=vendor_tasks)
        .prefetch_related("map_positions__location__map_info")
        .select_related("community__translation", "rank__translation")
    }
    items_targets_cache = {
        target.quest_id: target
        for target in CycleTaskTargetItem.objects.filter(
            quest__in=vendor_tasks,
        ).select_related("item__icon", "item__name_translation")
    }
    camps_targets_cache = {
        target.quest_id: target
        for target in CycleTaskTargetCamp.objects.filter(
            quest__in=vendor_tasks,
        ).select_related("map_position__location__map_info")
    }
    targets_cache: dict[int, CycleTaskTarget] = (
        stalker_targets_cache | items_targets_cache | camps_targets_cache
    )
    return targets_cache


def parse_task(
    db_task: CyclicQuest,
    targets_cache: dict[int, CycleTaskTarget],
) -> Quest:
    target = parse_target(db_task, targets_cache)
    rewards = [parse_item_reward(reward) for reward in db_task.itemreward_set.all()]
    for reward_money in db_task.moneyreward_set.all():
        rewards.append(TaskMoneyReward(reward_money.money))  # noqa: PERF401

    for _ in db_task.treasurereward_set.all():
        rewards.append(TreasureReward())  # noqa: PERF401

    for random_reward in db_task.questrandomreward_set.all():
        icon_ = random_reward.reward.icon.icon
        icon = IconData(icon_.url, icon_.width, icon_.height)
        reward = TaskRandomReward(
            count=random_reward.count,
            reward_name=random_reward.reward.description.rus,
            icon=icon,
        )
        rewards.append(reward)

    return Quest(target, rewards, db_task.text.rus if db_task.text else None)


def parse_target(
    db_task: CyclicQuest,
    targets_cache: dict[int, CycleTaskTarget],
) -> QuestTarget:
    #  pylint: disable=too-many-locals
    items_types = {
        QuestKinds.CHAIN,
        QuestKinds.FIND_MONSTER_PART,
        QuestKinds.FIND_ARTEFACT,
        QuestKinds.FIND_ITEM,
    }

    lager_types = {
        QuestKinds.ELIMINATE_CAMP,
        QuestKinds.DEFEND_CAMP,
    }

    stalker_types = {QuestKinds.KILL_STALKER}
    try:
        target = targets_cache[db_task.id]
    except KeyError as ex:
        msg = f"Нет цели для задания {db_task}"
        raise CycleTaskTarget.DoesNotExist(msg) from ex
    if db_task.type in stalker_types:
        if not isinstance(target, CycleTaskTargetStalker):
            raise ValueError
        stalker = target
        return _parse_stalker_target(db_task, stalker)
    if db_task.type in lager_types:
        if not isinstance(target, CycleTaskTargetCamp):
            raise ValueError
        target_camp = target
        return _parse_camp_target(db_task, target_camp)

    if db_task.type in items_types:
        if not isinstance(target, CycleTaskTargetItem):
            raise ValueError
        target_item = target.item.get_real_instance()
        target_cond_str: str | None = target.cond_str
        target_count = target.count or 1
        return _parse_target_item(target_cond_str, target_count, target_item)

    raise NotImplementedError


def _parse_target_item(
    target_cond_str: str | None,
    target_count: int,
    target_item: Item,
) -> QuestTarget:
    item_icon = _get_target_item_icon(target_item)

    item_info = ItemInfo(
        item_id=target_item.name,
        item_label=(
            target_item.name_translation.rus
            if target_item.name_translation
            else target_item.inv_name
        ),
        icon=item_icon,
    )

    if target_cond_str:
        if "," in target_cond_str:
            min_str, max_str = target_cond_str.split(",")
            state = ItemCondition(float(min_str.strip()), float(max_str.strip()))
        else:
            state = ItemCondition(float(target_cond_str.strip()), 100)
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


def _get_target_item_icon(target_item: Item) -> IconData | None:
    item_icon = None
    if target_item.icon:
        item_icon = IconData(
            target_item.icon.icon.url,
            target_item.icon.icon.width,
            target_item.icon.icon.height,
        )
    return item_icon


def _parse_camp_target(
    db_task: CyclicQuest,
    target_camp: CycleTaskTargetCamp,
) -> LagerTarget:
    camp_map_info = _spawn_item_to_map_info(
        target_camp.map_position,
        f"{db_task.game_code}_target_camp",
        str(target_camp),
    )
    return LagerTarget(camp_map_info)


def _parse_stalker_target(
    db_task: CyclicQuest,
    stalker: CycleTaskTargetStalker,
) -> StalkerTarget:
    possible_spawn_items = stalker.map_positions.all()
    maybe_map_points = [
        _spawn_item_to_map_info(item, f"{db_task.game_code}_stalker_{i}", "")
        for i, item in enumerate(possible_spawn_items)
    ]
    return StalkerTarget(
        str(stalker),
        [point for point in maybe_map_points if point is not None],
        stalker.rank.translation.rus,
        stalker.community.translation.rus,
    )


def _spawn_item_to_map_info(
    target_camp: MapPosition,
    unique_map_id: str,
    info_str: str,
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
                info_str=info_str,
            ),
        )
    return None


def parse_item_reward(reward: ItemReward) -> TaskReward:
    item_icon = None
    if reward.item.icon:
        item_icon = IconData(
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
