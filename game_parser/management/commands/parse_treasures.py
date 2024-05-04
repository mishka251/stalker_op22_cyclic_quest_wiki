import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.treasure import TreasureResource
from game_parser.models import Treasure

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "misc" / "treasure.ltx"

    _exclude_keys = {
        "list",
    }

    @atomic
    def handle(self, **options) -> None:
        Treasure.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        blocks = {k: v for k, v in results.items() if not self._should_exclude(k)}

        for quest_name, quest_data in blocks.items():
            print(quest_name)
            if not isinstance(quest_data, dict):
                raise TypeError
            resource = self._get_resource(quest_name, quest_data)
            resource.create_instance_from_data(quest_name, quest_data)
            if quest_data:
                logger.warning(f"unused data {quest_data} in {quest_name} {resource=}")

    def _get_resource(self, block_name: str, block_data: dict) -> TreasureResource:
        return TreasureResource()

    def _should_exclude(self, k: str) -> bool:
        return k in self._exclude_keys
