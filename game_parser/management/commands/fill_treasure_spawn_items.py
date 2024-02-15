import logging
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, ItemReward, BaseItem, GameStoryId, StorylineCharacter, Treasure, \
    CyclicQuest, SpawnItem
from game_parser.models import GameTask
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = Treasure.objects.count()
        for index, item in enumerate(Treasure.objects.all()):
            item.spawn_item = SpawnItem.objects.get(spawn_story_id=item.target)
            item.save()
            print(f'{index + 1}/{count}')
