import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.base_item import OutfitResource
from game_parser.models import Outfit

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "misc" / "outfit.ltx"

    _exclude_keys = {
        "without_outfit",
        "nano_resistance",
        "sect_mil_exoskeleton",
        "sect_mil_exoskeleton_add",
        "sect_mil_exoskeleton_adr",
    }

    @atomic
    def handle(self, **options) -> None:
        Outfit.objects.all().delete()

        known_bases = {
            "outfit": {},
        }

        parser = LtxParser(self.get_file_path(), known_extends=known_bases)
        results = parser.get_parsed_blocks()

        quest_blocks = {
            k: v
            for k, v in results.items()
            if k not in self._exclude_keys and not k.endswith("immunities")
        }

        resource = OutfitResource()

        for quest_name, quest_data in quest_blocks.items():
            print(quest_name)
            resource.create_instance_from_data(quest_name, quest_data)
            if quest_data:
                logger.warning(f"unused data {quest_data} in {quest_name}")
