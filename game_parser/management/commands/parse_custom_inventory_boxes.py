import json
import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import BaseItem, InventoryBox, ItemInTreasureBox

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "scripts" / "treasure"

    @atomic
    def handle(self, *args, **options) -> None:
        ItemInTreasureBox.objects.all().delete()
        InventoryBox.objects.all().delete()

        for file in self.get_file_path().iterdir():
            parser = LtxParser(file)
            results = parser.get_parsed_blocks()

            spawn = results.get("spawn")
            if not spawn:
                print("no spawn in file", file)
                continue
            item_with_count: dict[str, int] = {}
            if isinstance(spawn, list):
                item_with_count = {item: 1 for item in spawn}
            elif isinstance(spawn, dict):
                item_with_count = {
                    item: int(item_count) if item_count is not None else 1
                    for (item, item_count) in spawn.items()
                }
            raw_items_str = json.dumps(item_with_count)
            box = InventoryBox.objects.create(
                section_name=file.name[: -len(file.suffix)],
                source_file_name=str(file.relative_to(settings.OP22_GAME_DATA_PATH)),
                items_raw=raw_items_str,
            )

            for item_name, items_count in item_with_count.items():
                item = (
                    BaseItem.objects.filter(name=item_name).first()
                    or BaseItem.objects.filter(inv_name=item_name).first()
                )
                if not item:
                    print(f"Not found item {item_name=}")
                    continue
                ItemInTreasureBox.objects.create(
                    item=item,
                    box=box,
                    count=items_count,
                )
