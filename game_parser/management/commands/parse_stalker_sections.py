import logging
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.base_resource import BaseModelResource
from game_parser.logic.model_resources.stalker import StalkerResource
from game_parser.models import StalkerSection

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    STALKER_CLASSES = {
        "AI_STL_S",
    }

    def get_file_paths(self) -> list[Path]:
        base_path = settings.OP22_GAME_DATA_PATH
        dir_path = base_path / "config" / "creatures"
        return [
            dir_path / "m_stalker.ltx",
            dir_path / "m_person.ltx",
            dir_path / "immunities.ltx",
            dir_path / "damages.ltx",
            dir_path / "m_stalker_zombied.ltx",
            dir_path / "m_stalker_monolith.ltx",
            dir_path / "m_stalker_sniper.ltx",
            dir_path / "m_stalker_antisniper.ltx",
            dir_path / "m_stalker_murzo.ltx",
            dir_path / "m_stalker_sin.ltx",
            dir_path / "spawn_sections.ltx",
            dir_path / "spawn_sections_snp.ltx",
            dir_path / "vol_spawn.ltx",
        ]

    @atomic
    def handle(self, **options) -> None:
        print("Start cleaning")
        base_path = settings.OP22_GAME_DATA_PATH
        system_file = base_path / "config" / "system.ltx"
        StalkerSection.objects.all().delete()

        print("Cleaned")

        parser = LtxParser(system_file)
        results = parser.get_parsed_blocks()
        print("all_system parsed")
        assert isinstance(results, dict)
        for path in self.get_file_paths():
            parser = LtxParser(path, known_extends=results)
            results |= parser.get_parsed_blocks()

        existing_sections_keys = [k for k in results if isinstance(results[k], dict)]

        grouped_by_cls_dict = defaultdict(set)
        for section_name in existing_sections_keys:
            section = results[section_name]
            assert isinstance(section, dict)
            cls_name = section.get("class", "None")
            grouped_by_cls_dict[cls_name].add(section_name)
        for cls_, keys in grouped_by_cls_dict.items():
            print(cls_, len(keys))

        # TODO Проверить все секции на то, что всё есть в БД
        print("START FILLING")

        stalker_keys, stalkers = self._get_sections_by_class(
            results, grouped_by_cls_dict, self.STALKER_CLASSES
        )

        self._load_sections(stalkers, StalkerResource())

    def _load_sections(
        self, sections: dict[str, dict], resource: BaseModelResource
    ) -> None:
        for section_name, section in sections.items():
            resource.create_instance_from_data(section_name, section)

    def _get_sections_by_class(
        self, results, grouped_by_cls_dict, classes: set[str]
    ) -> tuple[set[str], dict[str, dict]]:
        ammo_keys = set()
        for key in classes:
            ammo_keys |= set(grouped_by_cls_dict[key])
        ammo = {
            ammo_key: results[ammo_key]
            for ammo_key in ammo_keys
            if ammo_key not in classes
        }
        return ammo_keys, ammo
