from pathlib import Path
# from xml.etree.ElementTree import Element, parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.models import GameTask, TaskObjective, MapLocationType, Dialog, Icon, StorylineCharacter
from game_parser.models.game_story.dialog import DialogPhrase
from PIL import Image
from django.core.files.images import ImageFile

logger = logging.getLogger(__name__)

DEFAULT_ENCODING = "windows-1251"


class Command(BaseCommand):
    TMP_DIR = Path('tmp')

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'gameplay'

    def get_files_paths(self, path: Path) -> list[Path]:
        paths = []
        for path in path.iterdir():
            if path.name.startswith('characters'):
                paths.append(path)

        return paths

    @atomic
    def handle(self, **options):
        StorylineCharacter.objects.all().delete()

        if not self.TMP_DIR.exists():
            self.TMP_DIR.mkdir()

        for file_path in self.get_files_paths(self.get_files_dir_path()):
            print(file_path)
            self._fix_fucking_incorrect_xml(file_path)
            root_node = parse(self._tml_file_name_for_xml(file_path)).getroot()
            comments = []
            for child_node in root_node:
                if child_node.tag == 'specific_character':
                    self._parse_character(child_node, comments)
                    comments = []
                elif isinstance(child_node, _Comment):
                    comments.append(child_node.text)
                else:
                    logger.warning(f'Unexpected node {child_node.tag} in {file_path}')

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

    def _replace_includes(self, content: str) -> str:
        import_regex = re.compile(r'#include "(?P<include_path>.*?)"')
        return re.sub(import_regex, self._get_included, content)

    def _get_included(self, m: re.Match) -> str:
        include_path = m.groupdict()['include_path']
        base_path = settings.OP22_GAME_DATA_PATH / 'config'
        target_path = base_path / include_path
        with open(target_path, 'r') as file:
            return file.read()

    def _parse_character(self, character_node: Element, comments: list[str]) -> None:
        # print(dialog_node)
        if character_node.tag != 'specific_character':
            logger.warning(f'Unexpected node {character_node.tag}')
            return
        character_id = character_node.attrib.pop('id')
        character_no_random = bool(character_node.attrib.pop('no_random', None))
        # team_default = int(character_node.attrib.pop('team_default',None))
        name = None
        icon_raw = None
        community_raw = None
        dialogs_raw = []
        rank = None
        reputation = None
        start_dialog = None
        visual = None
        supplies_raw = None
        class_raw = None
        crouch_type_raw = None
        snd_config_raw = None
        money_min_raw = None
        money_max_raw = None
        money_inf_raw = None
        terrain_sect_raw = None
        bio_raw = None
        team = None
        for child_node in character_node:
            if child_node.tag == 'name':
                name = child_node.text
            elif child_node.tag == 'icon':
                icon_raw = child_node.text
            elif child_node.tag == 'terrain_sect':
                terrain_sect_raw = child_node.text
            elif child_node.tag == 'bio':
                bio_raw = child_node.text
            elif child_node.tag == 'crouch_type':
                crouch_type_raw = child_node.text
            elif child_node.tag == 'snd_config':
                snd_config_raw = child_node.text
            elif child_node.tag == 'money':
                money_min_raw = child_node.attrib.pop("min")
                money_max_raw = child_node.attrib.pop("max")
                money_inf_raw = child_node.attrib.pop("infinitive")
            elif child_node.tag == 'visual':
                visual = child_node.text
            elif child_node.tag == 'class':
                class_raw = child_node.text
            elif child_node.tag == 'supplies':
                supplies_raw = child_node.text
            elif child_node.tag == 'rank':
                rank = int(child_node.text)
            elif child_node.tag == 'reputation':
                reputation = int(child_node.text)
            elif child_node.tag == 'community':
                community_raw = child_node.text
            elif child_node.tag == 'actor_dialog':
                dialogs_raw.append(child_node.text)
            elif child_node.tag == 'start_dialog':
                start_dialog = (child_node.text)
            elif isinstance(child_node, _Comment):
                pass
            elif child_node.tag == 'panic_threshold':
                pass
            elif child_node.tag == 'panic_treshold': #WTF??
                pass
            elif child_node.tag == 'map_icon':
                pass
            elif child_node.tag == 'team':
                team = child_node.text
            else:
                logger.warning(f'Unexpected node {child_node.tag} in character {character_id}')
        StorylineCharacter.objects.create(
            game_id=character_id,
            name=name,
            comments=';'.join(comments),
            icon_raw=icon_raw,
            community_default_raw=community_raw,
            dialogs_raw=';'.join(dialogs_raw),
            rank=rank,
            reputation=reputation,
            start_dialog_row=start_dialog,
            no_random=character_no_random,
            visual_raw=visual,
            supplies_raw=supplies_raw,
            class_raw=class_raw,
            crouch_type_raw=crouch_type_raw,
            snd_config_raw=snd_config_raw,
            money_min_raw=money_min_raw,
            money_max_raw=money_max_raw,
            money_inf_raw=money_inf_raw,
            terrain_sect_raw=terrain_sect_raw,
            bio_raw=bio_raw,
            team_raw = team,
        )
