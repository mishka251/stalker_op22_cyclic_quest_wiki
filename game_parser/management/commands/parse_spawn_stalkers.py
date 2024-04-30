from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser, TextLtxParser
from game_parser.models.spawn_item import Respawn, SingleStalkerSpawnItem, SpawnItem


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "spawns" / "all_cs" / "all.ltx"

    @atomic
    def handle(self, **options) -> None:
        Respawn.objects.all().delete()
        SingleStalkerSpawnItem.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        alife_files = results["alife"]
        level_files = alife_files["source_files"].split(",\n")
        print(level_files)
        respawns = []
        stalkers = []
        for level_file_name in level_files:
            level_file_path = self.get_file_path().parent / level_file_name
            print(level_file_path)
            level_parser = LtxParser(level_file_path)

            for section in level_parser.get_parsed_blocks().values():
                if section["section_name"] == "respawn":
                    respawn = self._create_respawn(level_file_name, section, level_file_path)
                    respawns.append(respawn)
                elif section["section_name"].startswith("stalker") and section["section_name"] != "stalker_outfit":
                    stalker = self._create_stalker(level_file_name, section, level_file_path)
                    stalkers.append(stalker)

        Respawn.objects.bulk_create(respawns, batch_size=2_000)
        SingleStalkerSpawnItem.objects.bulk_create(stalkers, batch_size=2_000)

    def _create_respawn(self, level_file_name: str, section: dict[str, str], path) -> Respawn:
        custom_data = TextLtxParser(path, section["custom_data"]).get_parsed_blocks().get("respawn", {})
        return Respawn(
            spawn_item=SpawnItem.objects.get(spawn_id=section["spawn_id"], location_txt=level_file_name),
            respawn_section_raw=custom_data["respawn_section"],
            max_spawn_raw=custom_data.get("max_spawn"),
            idle_spawn_raw=custom_data.get("idle_spawn"),
            conditions_raw=custom_data.get("conditions"),
        )

    def _create_stalker(self, level_file_name: str, section: dict[str, str], path) -> SingleStalkerSpawnItem:
        return SingleStalkerSpawnItem(
            spawn_item=SpawnItem.objects.get(spawn_id=section["spawn_id"], location_txt=level_file_name),
            character_profile_raw=section["character_profile"],
        )
