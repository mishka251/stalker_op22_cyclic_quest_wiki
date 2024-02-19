from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
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
            fixer = GSCXmlFixer(file_path)
            fixed_file_path = fixer.fix()
            root_node = parse(fixed_file_path).getroot()

            for game_dialogs in root_node:
                if game_dialogs.tag == 'info_portion':
                    self._parse_info_portion(game_dialogs)
                elif isinstance(game_dialogs, _Comment):
                   pass# dialog_comments.append(game_dialogs.text)
                    # logger.info(f'Comment {game_dialogs} {game_dialogs.text}')
                else:
                    logger.warning(f'Unexpected node {game_dialogs.tag} in {file_path}')

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
