import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.base_item import OtherResource
from game_parser.models import Other

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_main_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "defines.ltx"

    def _get_other_files_paths(self) -> list[Path]:
        base_path = settings.OP22_GAME_DATA_PATH
        return [
            base_path / "config" / "misc" / "items.ltx",
            base_path / "config" / "misc" / "arc.ltx",
            base_path / "config" / "misc" / "arhara_items.ltx",
            base_path / "config" / "misc" / "devices.ltx",
            base_path / "config" / "misc" / "ogg_player.ltx",
            base_path / "config" / "misc" / "quest_items.ltx",
            base_path / "config" / "misc" / "doc_view.ltx",
            base_path / "config" / "misc" / "nano_items.ltx",
        ]

    _exclude_keys = {
        # 'without_outfit',
        # 'nano_resistance',
        # 'sect_mil_exoskeleton',
        # 'sect_mil_exoskeleton_add',
        # 'sect_mil_exoskeleton_adr',
        "container_basic",
        "izom_globus_absorbation",
        "af_blood_tutorial",
        "amk_af_night_star",
        "kostya_af_gold_fish",
        "doc_view_end",
        "nano_med_activation",
        "nano_psi_activation",
        "nano_rad_activation",
        "nano_speed_activation",
    }

    @atomic
    def handle(self, **options) -> None:
        Other.objects.all().delete()

        main_parser = LtxParser(self.get_main_file_path())

        known_bases = main_parser.get_parsed_blocks()
        known_bases["af_blood"] = {}
        known_bases["af_night_star"] = {}
        known_bases["af_gold_fish"] = {}

        resource = OtherResource()

        for file_path in self._get_other_files_paths():
            parser = LtxParser(file_path, known_extends=known_bases)
            results = parser.get_parsed_blocks()
            known_bases |= results

            quest_blocks = {
                k: {**v}
                for k, v in results.items()
                if not self._should_exclude(k, v)
                # if k not in self._exclude_keys and not k.endswith('immunities')
            }

            for quest_name, quest_data in quest_blocks.items():
                print(quest_name)
                item = resource.create_instance_from_data(quest_name, quest_data)
                if quest_data:
                    logger.warning(f"unused data {quest_data} in {quest_name} {item=}")

    def _should_exclude(self, key: str, data: dict[str, str]) -> bool:
        if key in self._exclude_keys or key.endswith(
            ("immunities", "hud", "absorbation")
        ):
            return True
        cls = data.get("class")
        excluded_classes = {
            "C_HLCP_S",
            "O_INVBOX",
            "O_HLAMP",
            "O_PHYS_S",
            "O_SEARCH",
            "P_DSTRBL",
            "P_SKELET",
            "D_PDA",
            "TORCH_S",
            "SCRPTCAR",
            "SCRPTOBJ",
        }
        if cls in excluded_classes:
            return True
        return False
