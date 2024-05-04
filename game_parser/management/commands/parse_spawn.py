from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models.spawn_item import SpawnItem


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "spawns" / "all_cs" / "all.ltx"

    @atomic
    def handle(self, *args, **options) -> None:
        SpawnItem.objects.all().delete()

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
                item = self._create_item(level_file_name, section)
                spawn_items.append(item)
        SpawnItem.objects.bulk_create(spawn_items, batch_size=2_000)

    def _create_item(self, level_file_name: str, section: dict[str, str]) -> SpawnItem:
        return SpawnItem(
            section_name=section["section_name"],
            name=section["name"],
            position_raw=section["position"],
            spawn_id=section["spawn_id"],
            game_vertex_id=section["game_vertex_id"],
            location_txt=level_file_name,
            custom_data=section.get("custom_data"),
            character_profile_str=section.get("character_profile"),
            story_id=section.get("story_id"),
            spawn_story_id=section.get("spawn_story_id"),
        )
