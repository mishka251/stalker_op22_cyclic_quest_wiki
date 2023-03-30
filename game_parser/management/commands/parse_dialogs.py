from pathlib import Path
# from xml.etree.ElementTree import Element, parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.models import GameTask, TaskObjective, MapLocationType, Dialog
from game_parser.models.game_story.dialog import DialogPhrase

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
            if path.name.startswith('dialogs'):
                paths.append(path)
        # for (dir, _, files) in os.walk(path):
        #     for file_name in files:
        #         paths.append(Path(os.path.join(dir, file_name)))

        return paths

    @atomic
    def handle(self, **options):
        Dialog.objects.all().delete()
        DialogPhrase.objects.all().delete()

        if not self.TMP_DIR.exists():
            self.TMP_DIR.mkdir()

        for file_path in self.get_files_paths(self.get_files_dir_path()):
            if file_path.name == 'dialogs_vip_npc.xml':
                continue
            print(file_path)
            self._fix_fucking_incorrect_xml(file_path)
            # with open(self._tml_file_name_for_xml(file_path), 'r', encoding=DEFAULT_ENCODING) as tml_file:
            root_node = parse(self._tml_file_name_for_xml(file_path)).getroot()
            # print(root_node)
            dialog_comments = []

            for game_dialogs in root_node:
                if game_dialogs.tag == 'game_dialogs':
                    for maybe_dialog_node in game_dialogs:
                        if isinstance(maybe_dialog_node, _Comment):
                            # logger.info(f'Comment {maybe_dialog_node} {maybe_dialog_node.text}')
                            dialog_comments.append(maybe_dialog_node.text)
                        else:
                            self._parse_dialog(maybe_dialog_node, dialog_comments)
                            dialog_comments = []
                elif game_dialogs.tag == 'dialog':
                    self._parse_dialog(game_dialogs, dialog_comments)
                    dialog_comments = []
                elif isinstance(game_dialogs, _Comment):
                    dialog_comments.append(game_dialogs.text)
                    # logger.info(f'Comment {game_dialogs} {game_dialogs.text}')
                else:
                    logger.warning(f'Unexpected node {game_dialogs.tag} in {file_path}')

    def _tml_file_name_for_xml(self, source_file_path: Path) -> Path:
        return self.TMP_DIR / source_file_path.name

    def _fix_fucking_incorrect_xml(self, source_file_path: Path) -> None:
        with open(source_file_path, 'r', encoding=DEFAULT_ENCODING) as file:
            content = file.read()
        fixed_content = self._fix_broken_comments(content)
        # if source_file_path.name == 'dialogs_vip_npc.xml':
        #     fixed_content = self._add_root_tag(fixed_content)
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

    def _parse_dialog(self, dialog_node: Element, dialog_comments: list[str]) -> None:
        # print(dialog_node)
        if dialog_node.tag != 'dialog':
            logger.warning(f'Unexpected node {dialog_node.tag}')
        dialog_id = dialog_node.attrib.pop('id', None)
        if dialog_id is None:
            logger.warning(f'Unexpected id is None {dialog_node}')
            return
        # prio = dialog_node.attrib.pop('prio', None)
        dialog = Dialog.objects.create(game_id=dialog_id, comments_raw=';'.join(dialog_comments))
        preconditions = []
        has_info = []
        dont_has_info = []
        init_func = []
        # preconditions = []
        for child_node in dialog_node:
            # print(child_node)
            if child_node.tag == 'precondition':
                preconditions.append(child_node.text)
            elif child_node.tag == 'has_info':
                has_info.append(child_node.text)
            elif child_node.tag == 'dont_has_info':
                dont_has_info.append(child_node.text)
            elif child_node.tag == 'init_func':
                init_func.append(child_node.text)
            elif child_node.tag == 'phrase_list':
                self._parse_phrase_list(dialog, child_node)
            elif isinstance(child_node, _Comment):
                pass  # dialog_comments.append(game_dialogs.text)
            else:
                logger.warning(f'Unexpected game dialog child {child_node.tag} in {dialog_id}')
        dialog.precondition_raw = ';'.join(preconditions)
        dialog.dont_has_info_raw = ';'.join(dont_has_info)
        dialog.has_info_raw = ';'.join(has_info)
        dialog.init_func_raw = ';'.join(init_func)
        dialog.save()

    def _parse_phrase_list(self, dialog: Dialog, phrase_list_node: Element) -> None:
        for phrase_node in phrase_list_node:
            if phrase_node.tag == 'phrase':
                phrase_id = phrase_node.attrib.pop('id')
                phrase = DialogPhrase.objects.create(dialog=dialog, local_id=phrase_id)
                next = []
                precondition = []
                action = []
                give_info = []
                dont_has_info = []
                has_info = []
                disable_info = []
                disable = []
                text = None
                for child_node in phrase_node:
                    if child_node.tag == 'next':
                        next.append(child_node.text)
                    elif child_node.tag == 'text':
                        text = child_node.text
                    elif child_node.tag == 'precondition':
                        precondition.append(child_node.text)
                    elif child_node.tag == 'action':
                        action.append(child_node.text)
                    elif child_node.tag == 'give_info':
                        give_info.append(child_node.text)
                    elif child_node.tag == 'dont_has_info':
                        dont_has_info.append(child_node.text)
                    elif child_node.tag == 'has_info':
                        has_info.append(child_node.text)
                    elif child_node.tag == 'disable_info':
                        disable_info.append(child_node.text)
                    elif child_node.tag == 'disable':
                        disable.append(child_node.text)
                    elif isinstance(child_node, _Comment):
                        pass  # dialog_comments.append(game_dialogs.text)
                    else:
                        logger.warning(
                            f'Unexpected dialog phrase child {child_node.tag} in {dialog.game_id} {phrase_id}')
                phrase.text_id_raw = text
                phrase.next_ids_raw = ';'.join(next)
                phrase.actions_raw = ';'.join(action)
                phrase.precondition_raw = ';'.join(precondition)
                phrase.give_info_raw = ';'.join(give_info)
                phrase.has_info_raw = ';'.join(has_info)
                phrase.dont_has_info_raw = ';'.join(dont_has_info)
                phrase.disable_info_raw = ';'.join(disable_info)
                phrase.disable_raw = ';'.join(disable)
                phrase.save()
