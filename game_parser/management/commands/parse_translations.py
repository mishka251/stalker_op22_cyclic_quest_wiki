import logging
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.model_xml_loaders.translation import TranslationLoader
from game_parser.models import Translation

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_files_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "text"

    _exclude_files = {
        "cycle_task.xml",
        "dialog_exo_charge.xml",
        "string_table_ogg_flash_1.xml",
        "string_table_ogg_flash_10.xml",
        "string_table_ogg_flash_11.xml",
        "string_table_ogg_flash_12.xml",
        "string_table_ogg_flash_13.xml",
        "string_table_ogg_flash_14.xml",
        "string_table_ogg_flash_15.xml",
        "string_table_ogg_flash_16.xml",
        "string_table_ogg_flash_2.xml",
        "string_table_ogg_flash_3.xml",
        "string_table_ogg_flash_4.xml",
        "string_table_ogg_flash_5.xml",
        "string_table_ogg_flash_6.xml",
        "string_table_ogg_flash_7.xml",
        "string_table_ogg_flash_8.xml",
        "string_table_ogg_flash_9.xml",
        "string_table_ogg_flash_tracks.xml",
        "string_table_ogg_player_ui.xml",
    }

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        Translation.objects.all().delete()

        for file in self.get_files_path().iterdir():
            if file.name in self._exclude_files:
                continue
            print(f"{file=}")
            tree = ElementTree.parse(file)
            root = tree.getroot()

            if root.tag != "string_table":
                logger.warning(f"Wrong root {file}, {root}")
                continue
            TranslationLoader().load_bulk(root)
