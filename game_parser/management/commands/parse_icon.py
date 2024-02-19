from pathlib import Path
# from xml.etree.ElementTree import Element, parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
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
                elif child_node.tag == 'texture':
                    if image is None:
                        raise ValueError(f"image not first in file {file_path}")
                    self._parse_icon(child_node, image)
                    # dialog_comments = []
                # elif isinstance(child_node, _Comment):
                #     dialog_comments.append(child_node.text)
                    # logger.info(f'Comment {child_node} {child_node.text}')
                else:
                    logger.warning(f'Unexpected node {child_node.tag} in {file_path}')

    def _parse_icon(self, texture_node: Element, image: Image) -> None:
        # print(dialog_node)
        if texture_node.tag != 'texture':
            logger.warning(f'Unexpected node {texture_node.tag}')
            return
        texture_id = texture_node.attrib.pop('id')
        x = int(texture_node.attrib.pop('x'))
        y = int(texture_node.attrib.pop('y'))
        width = int(texture_node.attrib.pop('width'))
        height = int(texture_node.attrib.pop('height'))
        icon = Icon(name=texture_id)
        self._get_image(image, x, y, width, height, texture_id, icon)
        # Icon.objects.create(
        #     name=texture_id,
        #     icon=icon_image,
        # )

    def _get_item_image_coordinates(self, x:int, y:int, width:int, height:int) -> tuple[int, int, int, int]:
        inv_grid_x = x
        inv_grid_y = y

        inv_grid_width = width
        inv_grid_height = height

        left = inv_grid_x# * self.IMAGE_PART_WIDTH
        top = inv_grid_y #* self.IMAGE_PART_HEIGHT
        right = (inv_grid_x + inv_grid_width)# * self.IMAGE_PART_WIDTH
        bottom = (inv_grid_y + inv_grid_height) #* self.IMAGE_PART_HEIGHT

        return (left, top, right, bottom)

    def _get_image(self, image: Image, x:int, y:int, width:int, height:int, name: str, instance: Icon):
        box = self._get_item_image_coordinates(x, y, width, height)
        # logger.debug(f'{box=}')
        part = image.crop(box)
        tmp_file_name = 'tmp.png'
        part.save(tmp_file_name)
        with open(tmp_file_name, 'rb') as tmp_image:
            image_file = ImageFile(tmp_image, name=f'{name}_icon.png')
            instance.icon = image_file
            instance.save()
        # return image_file
