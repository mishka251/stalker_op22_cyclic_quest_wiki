import logging
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import KnownExtendsType, LtxParser, LtxParserResults
from game_parser.logic.model_resources.base_item import (
    BaseItemResource,
    CapsAnomResource,
    MonsterEmbrionResource,
    TrueArtefactResource,
)
from game_parser.models.items.artefact import CapsAnom, MonsterEmbrion, TrueArtefact

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_paths(self) -> list[Path]:
        base_path = settings.OP22_GAME_DATA_PATH
        return [
            base_path / "config" / "misc" / "artefacts.ltx",
            base_path / "config" / "misc" / "artefacts_amkzp.ltx",
            base_path / "config" / "misc" / "embrions.ltx",
        ]

    _exclude_keys = {
        "af_rusty_sea-urchin1_absorbation",
        "fosfor_light_hud",
        "artefact_spawn_zones",
        "embrion_activation",
        "af_activation_bold",
        "af_activation_gravi",
        "af_activation_mincer",
        "af_activation_electra",
        "af_activation_zharka",
        "af_activation_ameba",
        "zone_dog",
        "zone_krovosos",
        "zone_burer",
        "zone_zombie",
        "zone_snork",
        "zone_flesh",
        "zone_gigant",
        "zone_poltergeist",
        "zone_psevdodog",
        "zone_controller",
        "zone_chimera",
        "zone_boar",
        "zone_tushkano",
        "zone_psydog",
        "zone_cat",
        "zone_rat",
        "zone_tarakan",
        "zone_tarakan2",
        "zone_bloodsucker",
        "zone_bloodsucker2",
        "zone_deathclaw",
        "zone_fracture",
        "zone_bibliotekar",
        "zone_mono",
        "zone_tm",
        "zone_babka",
        "zone_ghost",
        "zone_kachok",
        "zone_big",
        "zone_jumper",
        "zone_electro",
        "zone_x_ray",
        "zone_wolf",
        "zone_lesnik",
        "cocoon",
        "caps_anom",
    }

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        # pylint: disable=too-many-locals
        TrueArtefact.objects.all().delete()
        MonsterEmbrion.objects.all().delete()
        CapsAnom.objects.all().delete()

        known_bases: KnownExtendsType = {
            "anomaly": {},
            "ARTEFACT": {
                "inv_grid_width": "1",
                "inv_grid_height": "1",
            },
        }

        for file_path in self.get_file_paths():

            parser = LtxParser(file_path, known_extends=known_bases)
            results = parser.get_parsed_blocks()
            if not isinstance(results, dict):
                raise TypeError
            blocks = self._get_arts_info(results)

            for quest_name, quest_data in blocks.items():
                print(quest_name)
                if not isinstance(quest_data, dict):
                    raise TypeError
                resource = self._get_resource(quest_data)
                item = resource.create_instance_from_data(quest_name, quest_data)
                if quest_data:
                    logger.warning(f"unused data {quest_data} in {quest_name} {item=}")

    def _get_arts_info(
        self,
        results: dict[str, list[str] | dict],
    ) -> dict[str, list[str] | dict]:
        blocks: LtxParserResults = {**results}
        block_names = list(blocks.keys())
        keys_to_exclude: set[str] = set()
        for block_name in block_names:
            block = blocks[block_name]
            if not isinstance(block, dict):
                raise TypeError
            if "hit_absorbation_sect" in block:
                hit_absorbation_sect_block_name: str = block.pop(
                    "hit_absorbation_sect",
                )
                hit_absorbation_sect = blocks[hit_absorbation_sect_block_name]
                if not isinstance(hit_absorbation_sect, dict):
                    raise TypeError
                block |= hit_absorbation_sect
                keys_to_exclude |= {hit_absorbation_sect_block_name}
        for key_to_exclude in keys_to_exclude:
            blocks.pop(key_to_exclude)
        return {k: v for k, v in blocks.items() if not self._should_exclude(k)}

    def _get_resource(self, block_data: dict) -> BaseItemResource:
        if block_data.get("cocoon", "false") == "true":
            return MonsterEmbrionResource()
        if block_data.get("caps_anom", "false") == "true":
            return CapsAnomResource()
        return TrueArtefactResource()

    def _should_exclude(self, k: str) -> bool:
        return k in self._exclude_keys or k.endswith("hud")
