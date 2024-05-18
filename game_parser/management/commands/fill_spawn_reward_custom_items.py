import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CustomSpawnItem, SpawnReward

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = SpawnReward.objects.count()
        for index, item in enumerate(SpawnReward.objects.all()):
            item.custom_spawn_section = CustomSpawnItem.objects.filter(
                name=item.raw_maybe_item,
            ).first()
            item.save()
            if index % 100 == 0:
                print(f"{index + 1}/{count}")
