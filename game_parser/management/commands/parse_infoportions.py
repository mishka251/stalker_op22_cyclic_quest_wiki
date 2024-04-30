import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.infoportion import InfoPortionLoader
from game_parser.models import InfoPortion

logger = logging.getLogger(__name__)



class Command(BaseCommand):
    TMP_DIR = Path("tmp")

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "gameplay"

    def get_files_paths(self, path: Path) -> list[Path]:
        paths = []
        for path in path.iterdir():
            if path.name.startswith("info"):
                paths.append(path)

        return paths

    @atomic
    def handle(self, **options):
        InfoPortion.objects.all().delete()
        for file_path in self.get_files_paths(self.get_files_dir_path()):
            print(file_path)
            fixer = GSCXmlFixer()
            fixed_file_path = fixer.fix(file_path)
            root_node = parse(fixed_file_path).getroot()
            InfoPortionLoader().load_bulk(root_node)

