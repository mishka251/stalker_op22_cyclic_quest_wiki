from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import CycleTaskVendor


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "misc" / "cycle_task.ltx"

    @atomic
    def handle(self, **options) -> None:
        CycleTaskVendor.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        vendor = results["vendor"]
        assert isinstance(vendor, dict)
        for vendor_id_raw, game_story_id_raw in vendor.items():
            vendor_id = int(vendor_id_raw)
            game_story_id = int(game_story_id_raw)
            CycleTaskVendor.objects.create(
                vendor_id=vendor_id,
                game_story_id_raw=game_story_id,
            )
