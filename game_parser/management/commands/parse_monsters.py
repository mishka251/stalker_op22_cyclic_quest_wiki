import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import KnownExtendsType, LtxParser
from game_parser.models import Monster

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "creatures" / "monsters.ltx"

    @atomic
    def handle(self, **options) -> None:
        Monster.objects.all().delete()

        known_bases: KnownExtendsType = {
            "base": {},
            "monster": {
                "monster": "true",
            },
        }

        parser = LtxParser(self.get_file_path(), known_extends=known_bases)
        results = parser.get_parsed_blocks()

        quest_blocks = {
            k: v
            for k, v in results.items()
            if isinstance(v, dict) and v.get("monster", "false") == "true"
        }

        for quest_name, quest_data in quest_blocks.items():
            print(quest_name)
            Monster.objects.create(
                section_name=quest_name,
                short_name=quest_data.get("short_name"),
                visual_str=quest_data.get("visual"),
                corpse_visual_str=quest_data.get("corpse_visual"),
                icon_str=quest_data.get("icon"),
                Spawn_Inventory_Item_Section=quest_data.get(
                    "Spawn_Inventory_Item_Section",
                ),
                Spawn_Inventory_Item_Probability=quest_data.get(
                    "Spawn_Inventory_Item_Probability",
                ),
                class_name=quest_data.get("class"),
                terrain=quest_data.get("terrain"),
                species=quest_data.get("species"),
                spec_rank=quest_data.get("spec_rank"),
            )
