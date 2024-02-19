import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse, Element, _Comment

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.models import Dialog
from game_parser.models.game_story.dialog import DialogPhrase

# from xml.etree.ElementTree import Element, parse

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
            fixer = GSCXmlFixer(file_path)
            fixed_file_path = fixer.fix()
            root_node = parse(fixed_file_path).getroot()
            dialog_comments = []

            for game_dialogs in root_node:
                if game_dialogs.tag == 'game_dialogs':
                    for maybe_dialog_node in game_dialogs:
                        if isinstance(maybe_dialog_node, _Comment):
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
