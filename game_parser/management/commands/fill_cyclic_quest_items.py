import logging
from typing import Optional

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CyclicQuest
from game_parser.models.items.base_item import BaseItem
from game_parser.models.quest import CyclicQuestItemReward, QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        CyclicQuestItemReward.objects.all().delete()
        quests_with_items = [
            QuestKinds.chain,
            QuestKinds.monster_part,
            QuestKinds.artefact,
            QuestKinds.find_item,
        ]
        count = CyclicQuest.objects.filter(type__in=quests_with_items).count()
        for index, quest in enumerate(
            CyclicQuest.objects.filter(type__in=quests_with_items)
        ):
            print(f"{index + 1}/{count}")
            quest.target_item = self._get_item_by_name(quest.target_str)
            quest.save()
        print("Стадия 2 - M2M")
        unfounded_rewards = set()
        quests_with_items_rewards = CyclicQuest.objects.exclude(
            reward_item_string__isnull=True
        ).exclude(reward_item_string="")
        count = quests_with_items_rewards.count()
        for index, quest in enumerate(quests_with_items_rewards):
            print(f"{index + 1}/{count}")
            items_info = self._parse_item_rewards(quest.reward_item_string)
            for item_name, item_count in items_info:
                item = self._get_item_by_name(item_name)
                if item is None:
                    unfounded_rewards.add(item_name)
                CyclicQuestItemReward.objects.create(
                    quest=quest,
                    item=item,
                    count=item_count,
                    raw_item=item_name,
                )

        unfounded_targets = set(
            CyclicQuest.objects.filter(
                target_item__isnull=True, type__in=quests_with_items
            ).values_list("target_str", flat=True),
        )
        print(f"{unfounded_targets=}")
        print(f"{unfounded_rewards=}")

    def _get_item_by_name(self, name: str) -> BaseItem | None:
        return (
            BaseItem.objects.filter(name=name).first()
            or BaseItem.objects.filter(inv_name=name).first()
        )

    def _parse_item_rewards(self, reward_item_string: str) -> list[tuple[str, int]]:
        parts = [s.strip() for s in reward_item_string.split(",")]
        prev_name = None
        result = []
        for part in parts:
            if part.isdigit():
                cnt = int(part)
                result.append((prev_name, cnt))
                prev_name = None
            else:
                if prev_name is not None:
                    result.append((prev_name, 1))
                prev_name = part
        if prev_name is not None:
            result.append((prev_name, 1))
        return result
