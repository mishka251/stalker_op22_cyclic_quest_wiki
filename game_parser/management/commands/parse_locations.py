import logging
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.location import LocationResource
from game_parser.models import Location

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "game_levels.ltx"

    _exclude_keys = {
        "levels",
    }

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        Location.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        blocks = {k: v for k, v in results.items() if not self._should_exclude(k)}
        resource = LocationResource()

        for quest_name, quest_data in blocks.items():
            print(quest_name)
            if not isinstance(quest_data, dict):
                raise TypeError
            item = resource.create_instance_from_data(quest_name, quest_data)
            if quest_data:
                logger.warning(f"unused data {quest_data} in {quest_name} {item=}")

    def _should_exclude(self, k: str) -> bool:
        return k in self._exclude_keys
