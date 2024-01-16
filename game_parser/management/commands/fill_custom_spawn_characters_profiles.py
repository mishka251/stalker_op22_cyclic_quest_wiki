import logging
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, ItemReward, BaseItem, GameStoryId, StorylineCharacter, Treasure, \
    CyclicQuest, SpawnItem, CustomSpawnItem
from game_parser.models import GameTask
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = CustomSpawnItem.objects.count()
        for index, item in enumerate(CustomSpawnItem.objects.all()):
            if item.character_profile_str:
                item.character_profile = StorylineCharacter.objects.filter(game_id=item.character_profile_str).first()
                item.save()
            print(f'{index + 1}/{count}')
