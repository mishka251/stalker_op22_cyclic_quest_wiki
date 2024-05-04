from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models.spawn_item import CustomSpawnItem


class Command(BaseCommand):

    def get_file_paths(self) -> list[Path]:
        base_path = settings.OP22_GAME_DATA_PATH
        dir_path = base_path / "config" / "creatures"
        return [
            dir_path / "spawn_sections.ltx",
            dir_path / "spawn_sections_snp.ltx",
            dir_path / "vol_spawn.ltx",
        ]

    base_sections = {
        "stalker_sniper": {"__parent": "stalker_sniper"},
        "stalker": {"__parent": "stalker"},
        "monster": {"__parent": "monster"},
        "physic_object": {"__parent": "physic_object"},
        "stalker_monolith": {"__parent": "stalker_monolith"},
        "stalker_zombied": {"__parent": "stalker_zombied"},
        "stalker_sakharov": {"__parent": "stalker_sakharov"},
        "stalker_fresh_zombied": {"__parent": "stalker_fresh_zombied"},
        "stalker_antisniper": {"__parent": "stalker_antisniper"},
        "boar_normal": {"__parent": "boar_normal"},
        "boar_strong": {"__parent": "boar_strong"},
        "pseudodog_strong": {"__parent": "pseudodog_strong"},
        "pseudodog_big": {"__parent": "pseudodog_big"},
        "volkodav": {"__parent": "volkodav"},
        "molerat": {"__parent": "molerat"},
        "kikimora": {"__parent": "kikimora"},
        "boar_kachok": {"__parent": "boar_kachok"},
        "vypolzen_red": {"__parent": "vypolzen_red"},
        "snork_jumper": {"__parent": "snork_jumper"},
        "snork_stronger": {"__parent": "snork_stronger"},
        "snork_nosach": {"__parent": "snork_nosach"},
        "lican": {"__parent": "lican"},
        "vehicle_btr": {"__parent": "vehicle_btr"},
        "inventory_box": {"__parent": "inventory_box"},
        "stalker_trader": {"__parent": "stalker_trader"},
        "bloodsucker_weak": {"__parent": "bloodsucker_weak"},
        "controller_swamp": {"__parent": "controller_swamp"},
        "m_controller_old": {"__parent": "m_controller_old"},
        "m_controller_normal_fat": {"__parent": "m_controller_normal_fat"},
        "m_controller_normal": {"__parent": "m_controller_normal"},
        "m_controller_old_fat": {"__parent": "m_controller_old_fat"},
        "controller_senator": {"__parent": "controller_senator"},
        "controller_babka": {"__parent": "controller_babka"},
        "psyonik": {"__parent": "psyonik"},
        "burer_normal": {"__parent": "burer_normal"},
        "burer_electro": {"__parent": "burer_electro"},
        "chimera_wolf": {"__parent": "chimera_wolf"},
        "arahnid": {"__parent": "arahnid"},
        "bibliotekar": {"__parent": "bibliotekar"},
        "bibliotekar_black": {"__parent": "bibliotekar_black"},
        "vodjanoj": {"__parent": "vodjanoj"},
        "zombie_ghost": {"__parent": "zombie_ghost"},
        "tushkano_normal": {"__parent": "tushkano_normal"},
        "tushkano_strong": {"__parent": "tushkano_strong"},
        "m_poltergeist_strong_flame": {"__parent": "m_poltergeist_strong_flame"},
        "m_poltergeist_normal_tele": {"__parent": "m_poltergeist_normal_tele"},
        "polter_xray": {"__parent": "polter_xray"},
        "electro_polter": {"__parent": "electro_polter"},
        "deathclaw_phantom": {"__parent": "deathclaw_phantom"},
        "bibliotekar_black_volna": {"__parent": "bibliotekar_black_volna"},
        "deathclaw_volna": {"__parent": "deathclaw_volna"},
        "new_hell_volna": {"__parent": "new_hell_volna"},
        "stalker_murzo": {"__parent": "stalker_murzo"},
        "rat_normal": {"__parent": "rat_normal"},
        "tarakan_normal": {"__parent": "tarakan_normal"},
        "m_cat_e": {"__parent": "m_cat_e"},
        "snork_normal": {"__parent": "snork_normal"},
        "m_burer_e": {"__parent": "m_burer_e"},
        "bloodsucker_strong": {"__parent": "bloodsucker_strong"},
        "stalker_sin": {"__parent": "stalker_sin"},
        "wpn_pkm": {"__parent": "wpn_pkm"},
        "new_hell": {"__parent": "new_hell"},
        "bloodsucker_super_strong": {"__parent": "bloodsucker_super_strong"},
        "bloodsucker_mil": {"__parent": "bloodsucker_mil"},
        "bloodsucker_effector": {"__parent": "bloodsucker_effector"},
        "flesh_meat": {"__parent": "flesh_meat"},
        "flesh_weak": {"__parent": "flesh_weak"},
        "chimera_weak": {"__parent": "chimera_weak"},
        "wpn_vihlop": {"__parent": "wpn_vihlop"},
        "wpn_peceneg": {"__parent": "wpn_peceneg"},
        "stalker_inferno_electric": {"__parent": "stalker_inferno_electric"},
        "s_inventory_box_vzn": {"__parent": "s_inventory_box_vzn"},
        "bloodsucker_hell": {"__parent": "bloodsucker_hell"},
        "snork_weak": {"__parent": "snork_weak"},
    }

    @atomic
    def handle(self, *args, **options) -> None:
        CustomSpawnItem.objects.all().delete()
        spawn_items = []
        for file in self.get_file_paths():
            print(file)
            parser = LtxParser(file, known_extends=self.base_sections)

            for section_id, section in parser.get_parsed_blocks().items():
                if not isinstance(section, dict):
                    raise TypeError
                section_parent = section["__parent"]
                item = self._create_item(section_id, section_parent, section)
                spawn_items.append(item)
        CustomSpawnItem.objects.bulk_create(spawn_items, batch_size=2_000)

    def _create_item(
        self,
        name: str,
        section_parent: str,
        section: dict[str, str],
    ) -> CustomSpawnItem:
        return CustomSpawnItem(
            section_name=section_parent,
            name=name,
            custom_data=section.get("custom_data"),
            character_profile_str=section.get("character_profile"),
            spec_rank_str=section.get("spec_rank"),
            community_str=section.get("community"),
            visual_str=section.get("visual"),
        )
