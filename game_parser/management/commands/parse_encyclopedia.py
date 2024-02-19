import logging
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse, Element

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.models import EncyclopediaGroup, EncyclopediaArticle, Translation, Icon, Artefact

from pathlib import Path
# from xml.etree.ElementTree import Element, parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.models import GameTask, TaskObjective, MapLocationType, Dialog, Icon
from game_parser.models.game_story.dialog import DialogPhrase
from PIL import Image
from django.core.files.images import ImageFile


logger = logging.getLogger(__name__)
DEFAULT_ENCODING = "windows-1251"

class Command(BaseCommand):
    TMP_DIR = Path('tmp')

    def get_file_path(self):
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'gameplay' / 'encyclopedia.xml'

    @atomic
    def handle(self, **options):
        EncyclopediaGroup.objects.all().delete()
        EncyclopediaArticle.objects.all().delete()
        fixer = GSCXmlFixer(self.get_file_path())
        fixed_file_path = fixer.fix()
        root_node = parse(fixed_file_path).getroot()
        for maybe_article in root_node:
            if maybe_article.tag == 'article':
                print(maybe_article)
                self._parse_article(maybe_article)

    def _parse_article(self, article_node: Element) -> None:
        game_id = article_node.attrib.pop('id', None)
        name = article_node.attrib.pop('name', None)
        group_name = article_node.attrib.pop('group', None)
        ltx_str = None
        text = None
        icon = None
        for child_node in article_node:
            # print(child_node)
            if child_node.tag == 'ltx':
                ltx_str = child_node.text
            elif child_node.tag == 'text':
                text = child_node.text
            elif child_node.tag == 'texture':
                icon = self._parse_icon(child_node)
            else:
                logger.warning(f'Unexpected game info_portion child {child_node.tag} in {game_id}')
        group = EncyclopediaGroup.objects.get_or_create(
            name=group_name,
            defaults={"name_translation": Translation.objects.filter(code=group_name).first()},
        )[0]
        artefact = None
        if ltx_str:
            artefact = Artefact.objects.filter(name=ltx_str).first()
        article = EncyclopediaArticle.objects.create(
            game_id=game_id,
            name=name,
            name_translation=Translation.objects.filter(code=name).first(),
            group_name=group_name,
            group=group,
            ltx_str=ltx_str,
            icon=icon,
            text=text,
            text_translation=Translation.objects.filter(code=text).first(),
            artefact=artefact,
        )

    def _parse_icon(self, texture_node: Element) -> Icon:
        # print(dialog_node)
        # if texture_node.tag != 'texture':
        #     logger.warning(f'Unexpected node {texture_node.tag}')
        #     return

        # texture_id = texture_node.attrib.pop('id')
        x = texture_node.attrib.pop('x', None)
        if x is None:
            texture_id = texture_node.text
            return Icon.objects.get(name=texture_id)
        x = int(x)
        y = int(texture_node.attrib.pop('y'))
        width = int(texture_node.attrib.pop('width'))
        height = int(texture_node.attrib.pop('height'))
        image_file = texture_node.text+".dds"
        base_path = settings.OP22_GAME_DATA_PATH
        file_path = base_path/"textures"/image_file
        image = Image.open(file_path)
        texture_id = image_file
        icon = Icon(name=texture_id)
        self._get_image(image, x, y, width, height, texture_id, icon)
        return icon

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
        return instance

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

