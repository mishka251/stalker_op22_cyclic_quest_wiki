import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CustomSpawnItem, GameStoryId

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = GameStoryId.objects.count()
        for index, item in enumerate(GameStoryId.objects.all()):
            item.spawn_section_custom = CustomSpawnItem.objects.filter(
                name=item.section_name,
            ).first()
            item.save()
            print(f"{index + 1}/{count}")
