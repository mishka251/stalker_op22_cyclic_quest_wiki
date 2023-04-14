import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.treasure import TreasureResource
from game_parser.models import Treasure, GameStoryId

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'game_story_ids.ltx'

    @atomic
    def handle(self, **options):
        GameStoryId.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        blocks = {
            k: v
            for k, v in results.items()
        }

        block: dict[str, str] = blocks['story_ids']
        # print(block)
        for game_id_raw, section_name_raw in block.items():
            game_id = int(game_id_raw)
            section_name = section_name_raw.strip('"')
            # print(game_id, section_name)
            GameStoryId.objects.create(
                story_id=game_id,
                section_name=section_name,
            )


