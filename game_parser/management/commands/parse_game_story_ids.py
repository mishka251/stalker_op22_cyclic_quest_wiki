import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import GameStoryId

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "game_story_ids.ltx"

    @atomic
    def handle(self, **options) -> None:
        GameStoryId.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()
        if not isinstance(results, dict):
            raise TypeError
        if not isinstance(results["story_ids"], dict):
            raise TypeError
        block: dict[str, str] = results["story_ids"]
        for game_id_raw, section_name_raw in block.items():
            game_id = int(game_id_raw)
            section_name = section_name_raw.strip('"')
            GameStoryId.objects.create(
                story_id=game_id,
                section_name=section_name,
            )
