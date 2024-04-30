import logging
from pathlib import Path

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
    def handle(self, **options) -> None:
        Location.objects.all().delete()

        known_bases = {}

        parser = LtxParser(self.get_file_path(), known_extends=known_bases)
        results = parser.get_parsed_blocks()

        blocks = {k: v for k, v in results.items() if not self._should_exclude(k)}

        for quest_name, quest_data in blocks.items():
            print(quest_name)
            resource = self._get_resource(quest_name, quest_data)
            item = resource.create_instance_from_data(quest_name, quest_data)
            if quest_data:
                logger.warning(f"unused data {quest_data} in {quest_name} {item=}")

    def _get_resource(self, block_name: str, block_data: dict) -> LocationResource:
        return LocationResource()

    def _should_exclude(self, k: str) -> bool:
        return k in self._exclude_keys
