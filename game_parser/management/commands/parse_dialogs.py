import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.dialog import DialogLoader
from game_parser.models import Dialog
from game_parser.models.game_story.dialog import DialogPhrase

# from xml.etree.ElementTree import Element, parse

logger = logging.getLogger(__name__)

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
            fixer = GSCXmlFixer()
            fixed_file_path = fixer.fix(file_path)
            root_node = parse(fixed_file_path).getroot()
            DialogLoader().load_bulk(root_node)