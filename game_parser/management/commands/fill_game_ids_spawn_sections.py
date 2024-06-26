import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import GameStoryId, SpawnItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = GameStoryId.objects.count()
        for index, item in enumerate(GameStoryId.objects.all()):
            item.spawn_section = (
                SpawnItem.objects.filter(story_id=item.story_id).first()
                or SpawnItem.objects.filter(spawn_story_id=item.story_id).first()
            )
            item.save()
            if index % 50 == 0:
                print(f"{index+1}/{count}")
