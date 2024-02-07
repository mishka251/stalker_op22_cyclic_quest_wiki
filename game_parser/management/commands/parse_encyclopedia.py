import logging
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse, Element

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
        self._fix_fucking_incorrect_xml(self.get_file_path())
        root_node = parse(self._tml_file_name_for_xml(self.get_file_path())).getroot()
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

    def _tml_file_name_for_xml(self, source_file_path: Path) -> Path:
        return self.TMP_DIR / source_file_path.name

    def _fix_fucking_incorrect_xml(self, source_file_path: Path) -> None:
        with open(source_file_path, 'r', encoding=DEFAULT_ENCODING) as file:
            content = file.read()
        fixed_content = self._fix_broken_comments(content)
        with open(self._tml_file_name_for_xml(source_file_path), 'w', encoding=DEFAULT_ENCODING) as tml_file:
            tml_file.write(fixed_content)

    def _add_root_tag(self, content: str) -> str:
        return f'<xml>{content}</xml>'
    def _fix_broken_comments(self, content: str) -> str:
        current_content = ''
        fixed_content = content
        xml_comment_re = re.compile(r'<!--(?P<before>.*?)-{2,}(?P<after>.*)-->')
        while fixed_content != current_content:
            current_content = fixed_content
            fixed_content = re.sub(xml_comment_re, r'<!--\g<before> \g<after>-->', current_content)
        xml_comment2_re = re.compile(r'<!--[\s-]*(?P<comment>.*?)[\s-]*-->')
        fixed_content = re.sub(xml_comment2_re, r'<!-- \g<comment> -->', fixed_content)
        return fixed_content