import os
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models.spawn_item import NpcLogicConfig


class Command(BaseCommand):

    def get_configs_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config"

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "scripts"

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        # pylint: disable=too-many-locals
        NpcLogicConfig.objects.all().delete()
        root_dir = self.get_file_path()
        spawn_items = []
        file_paths = []
        print("start")
        for walk in os.walk(root_dir):
            (dirpath, _, filenames) = walk
            for filename in filenames:
                file_path = root_dir / dirpath / filename
                file_paths.append(file_path)
        print(f"Collected {len(file_paths)} files")
        for i, file_path in enumerate(file_paths):
            print(f"{i}/{len(file_paths)}  {file_path}")
            parser = LtxParser(file_path)
            results = parser.get_parsed_blocks()
            if not isinstance(results, dict):
                raise TypeError
            dict_result = {k: v for k, v in results.items() if isinstance(v, dict)}
            if "logic" not in results:
                continue

            item = self._create_item(file_path, dict_result)
            spawn_items.append(item)
        print(f"Creating {len(spawn_items)} possible npc configs")
        NpcLogicConfig.objects.bulk_create(spawn_items, batch_size=2_000)

    def _create_item(
        self,
        file_path: Path,
        section: dict[str, dict[str, str]],
    ) -> NpcLogicConfig:
        trade_file_name = section["logic"].get("trade")
        return NpcLogicConfig(
            name=file_path.name,
            source_file_name=str(file_path.relative_to(self.get_configs_path())),
            trade_file_name=trade_file_name,
        )
