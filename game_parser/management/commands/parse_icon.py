import logging
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse
from PIL import Image

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.icon import IconLoader
from game_parser.models import Icon

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    TMP_DIR = Path("tmp")
    IMAGE_PART_WIDTH = 50
    IMAGE_PART_HEIGHT = 50

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "ui"

    def get_files_paths(self, path: Path) -> list[Path]:
        paths = []
        for aub_path in path.iterdir():
            if aub_path.name.startswith("ui_npc") or aub_path.name in {
                "ui_arhara_unique.xml",
                "ui_icons_npc.xml",
                "ui_iconstotal.xml",
                "ui_iconstotal2.xml",
                "ui_npc_chess.xml",
                "ui_npc_monster.xml",
                "ui_npc_snp.xml",
                "ui_npc_unique.xml",
                "ui_npc_unique_2.xml",
            }:
                paths.append(aub_path)  # noqa: PERF401

        return paths

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        Icon.objects.all().delete()

        if not self.TMP_DIR.exists():
            self.TMP_DIR.mkdir()

        for file_path in self.get_files_paths(self.get_files_dir_path()):
            print(file_path)
            fixer = GSCXmlFixer()
            fixed_file_path = fixer.fix(file_path)
            root_node = parse(fixed_file_path).getroot()
            image = None
            for child_node in root_node:
                if child_node.tag == "file_name":
                    if child_node.text is None:
                        raise TypeError
                    image_file_path = (
                        settings.OP22_GAME_DATA_PATH
                        / "textures"
                        / (child_node.text + ".dds")
                    )
                    image = Image.open(image_file_path)
            if image is None:
                msg = f"No image in {file_path}"
                raise ValueError(msg)
            loader = IconLoader(image)
            loader.load_bulk(root_node)
