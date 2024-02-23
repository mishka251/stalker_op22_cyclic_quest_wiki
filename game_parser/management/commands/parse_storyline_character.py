import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.storyline_character import StorylineCharacterLoader
from game_parser.models import StorylineCharacter

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
            fixer = GSCXmlFixer(file_path)
            fixed_file_path = fixer.fix()
            root_node = parse(fixed_file_path).getroot()
            StorylineCharacterLoader().load_bulk(root_node)
