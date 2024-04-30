import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CyclicQuest, QuestRandomReward
from game_parser.models.quest import QuestRandomRewardThrough

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = CyclicQuest.objects.count()
        QuestRandomRewardThrough.objects.all().delete()
        for index, quest in enumerate(CyclicQuest.objects.all()):
            if not quest.random_rewards_string:
                continue

            parts = [item.strip() for item in quest.random_rewards_string.split(",")]
            items = list(zip(parts[::2], parts[1::2]))

            for (reward_index, reward_count) in items:
                reward_id = f"random_{reward_index}"
                QuestRandomRewardThrough.objects.create(
                    quest=quest,
                    count=int(reward_count),
                    reward=QuestRandomReward.objects.get(name=reward_id)
                )
            print(f"{index+1}/{count}")

