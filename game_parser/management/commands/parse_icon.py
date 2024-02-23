from pathlib import Path
# from xml.etree.ElementTree import Element, parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.icon import IconLoader
from game_parser.models import GameTask, TaskObjective, MapLocationType, Dialog, Icon
from game_parser.models.game_story.dialog import DialogPhrase
from PIL import Image
from django.core.files.images import ImageFile

logger = logging.getLogger(__name__)

DEFAULT_ENCODING = "windows-1251"


class Command(BaseCommand):
    TMP_DIR = Path('tmp')
    IMAGE_PART_WIDTH = 50
    IMAGE_PART_HEIGHT = 50

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'ui'

    def get_files_paths(self, path: Path) -> list[Path]:
        paths = []
        for path in path.iterdir():
            if path.name.startswith('ui_npc')\
                    or path.name in {
                'ui_arhara_unique.xml',
                'ui_icons_npc.xml',
                'ui_iconstotal.xml',
                'ui_iconstotal2.xml',
                'ui_npc_chess.xml',
                'ui_npc_monster.xml',
                'ui_npc_snp.xml',
                'ui_npc_unique.xml',
                'ui_npc_unique_2.xml',
            }:
                paths.append(path)
        # for (dir, _, files) in os.walk(path):
        #     for file_name in files:
        #         paths.append(Path(os.path.join(dir, file_name)))

        return paths

    @atomic
    def handle(self, **options):
        Icon.objects.all().delete()

        if not self.TMP_DIR.exists():
            self.TMP_DIR.mkdir()

        for file_path in self.get_files_paths(self.get_files_dir_path()):
            print(file_path)
            fixer = GSCXmlFixer(file_path)
            fixed_file_path = fixer.fix()
            root_node = parse(fixed_file_path).getroot()
            image = None
            for child_node in root_node:
                if child_node.tag == 'file_name':
                    image_file_path = settings.OP22_GAME_DATA_PATH/'textures'/(child_node.text+'.dds')
                    image = Image.open(image_file_path)
            loader = IconLoader(image)
            loader.load_bulk(root_node)
