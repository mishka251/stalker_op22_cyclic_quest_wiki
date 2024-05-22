import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import GameVertex, SpawnReward

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = SpawnReward.objects.count()
        for index, item in enumerate(SpawnReward.objects.all()):
            item.game_vertex_obj = GameVertex.objects.filter(
                vertex_id=item.game_vertex_id,
            ).first()
            item.save()
            if index % 100 == 0:
                print(f"{index + 1}/{count}")
