from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.models import InfoPortion

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
            if path.name.startswith('info'):
                paths.append(path)

        return paths

    @atomic
    def handle(self, **options):
        InfoPortion.objects.all().delete()

        if not self.TMP_DIR.exists():
            self.TMP_DIR.mkdir()

        for file_path in self.get_files_paths(self.get_files_dir_path()):

            print(file_path)
            self._fix_fucking_incorrect_xml(file_path)
            # with open(self._tml_file_name_for_xml(file_path), 'r', encoding=DEFAULT_ENCODING) as tml_file:
            root_node = parse(self._tml_file_name_for_xml(file_path)).getroot()

            for game_dialogs in root_node:
                if game_dialogs.tag == 'info_portion':
                    self._parse_info_portion(game_dialogs)
                elif isinstance(game_dialogs, _Comment):
                   pass# dialog_comments.append(game_dialogs.text)
                    # logger.info(f'Comment {game_dialogs} {game_dialogs.text}')
                else:
                    logger.warning(f'Unexpected node {game_dialogs.tag} in {file_path}')

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

    # def _fix_fuck

    def _parse_info_portion(self, dialog_node: Element) -> None:
        info_portion_id = dialog_node.attrib.pop('id', None)
        info_portion = InfoPortion.objects.create(game_id=info_portion_id )
        article_raw = []
        disable_raw = []
        task_raw = []
        actions_raw = []
        # preconditions = []
        for child_node in dialog_node:
            # print(child_node)
            if child_node.tag == 'article':
                article_raw.append(child_node.text)
            elif child_node.tag == 'disable':
                disable_raw.append(child_node.text)
            elif child_node.tag == 'task':
                task_raw.append(child_node.text)
            elif child_node.tag == 'action':
                actions_raw.append(child_node.text)
            # elif child_node.tag == 'phrase_list':
            #     self._parse_phrase_list(info_portion, child_node)
            elif isinstance(child_node, _Comment):
                pass  # dialog_comments.append(game_dialogs.text)
            else:
                logger.warning(f'Unexpected game info_portion child {child_node.tag} in {info_portion_id}')
        info_portion.article_raw = ';'.join(article_raw)
        info_portion.disable_raw = ';'.join(disable_raw)
        info_portion.task_raw = ';'.join(task_raw)
        info_portion.actions_raw = ';'.join(actions_raw)
        info_portion.save()
