from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser, TextLtxParser
from game_parser.models.spawn_item import CampInfo, SpawnItem


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "spawns" / "all.ltx"

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        CampInfo.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        alife_files = results["alife"]
        if not isinstance(alife_files, dict):
            raise TypeError
        if not isinstance(alife_files["source_files"], str):
            raise TypeError
        level_files = alife_files["source_files"].split(",\n")
        print(level_files)
        spawn_items = []
        for level_file_name in level_files:
            level_file_path = self.get_file_path().parent / level_file_name
            print(level_file_path)
            level_parser = LtxParser(level_file_path)

            for section in level_parser.get_parsed_blocks().values():
                if not isinstance(section, dict):
                    raise TypeError
                if section["section_name"] == "smart_terrain":

                    item = self._create_item(level_file_name, section, level_file_path)
                    spawn_items.append(item)
        CampInfo.objects.bulk_create(spawn_items, batch_size=2_000)

    def _create_item(
        self,
        level_file_name: str,
        section: dict[str, str],
        path: Path,
    ) -> CampInfo:
        custom_data = (
            TextLtxParser(path, section["custom_data"])
            .get_parsed_blocks()
            .get("smart_terrain", {})
        )
        if not isinstance(custom_data, dict):
            raise TypeError
        return CampInfo(
            spawn_item=SpawnItem.objects.get(
                spawn_id=section["spawn_id"],
                location_txt=level_file_name,
            ),
            type=custom_data.get("type"),
            capacity=custom_data.get("capacity"),
            cond_raw=custom_data.get("cond"),
            communities_raw=custom_data.get("communities"),
            stay_str=custom_data.get("stay"),
            groups_str=custom_data.get("groups"),
        )
