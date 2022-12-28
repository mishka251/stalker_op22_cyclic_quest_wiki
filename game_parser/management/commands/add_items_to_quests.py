import logging
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CyclicQuest
from game_parser.models.items.base_item import BaseItem
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        quests_with_items = [
            QuestKinds.chain,
            QuestKinds.monster_part,
            QuestKinds.artefact,
            QuestKinds.find_item,
        ]
        count = CyclicQuest.objects.filter(type__in=quests_with_items).count()
        for index, quest in enumerate(CyclicQuest.objects.filter(type__in=quests_with_items)):
            print(f'{index+1}/{count}')
            quest.target_item = BaseItem.objects.filter(name=quest.target_str).first()
            quest.save()
        print('Стадия 2 - M2M')
        unfounded_rewards = set()
        for index, quest in enumerate(CyclicQuest.objects.filter(type__in=quests_with_items)):
            print(f'{index + 1}/{count}')
            if quest.reward_item_string is None:
                continue
            rewards_names = set(map(lambda s: s.strip(), quest.reward_item_string.split(',')))
            rewards_items = BaseItem.objects.filter(name__in=rewards_names)

            unfounded = set(rewards_items.values_list('name', flat=True)) - set(rewards_names)
            unfounded_rewards |= unfounded
            quest.reward_items.set(rewards_items)

        unfounded_targets = set(
            CyclicQuest.objects
            .filter(target_item__isnull=True, type__in=quests_with_items)
            .values_list('target_str', flat=True)
        )
        print(f'{unfounded_targets=}')
        print(f'{unfounded_rewards=}')
