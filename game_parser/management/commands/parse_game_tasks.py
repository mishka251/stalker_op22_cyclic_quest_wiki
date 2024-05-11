import logging
from pathlib import Path
from xml.etree.ElementTree import parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.game_task import GameTaskLoader
from game_parser.models import GameTask, TaskObjective

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "gameplay"

    def get_files_path(self) -> Path:
        return self.get_files_dir_path() / "game_tasks.xml"

    @atomic
    def handle(self, *args, **options) -> None:
        GameTask.objects.all().delete()
        TaskObjective.objects.all().delete()

        file_path = self.get_files_path()
        print(file_path)
        fixer = GSCXmlFixer(encoding="cp-1251")
        fixed_file_path = fixer.fix(file_path)
        root_node = parse(fixed_file_path).getroot()
        GameTaskLoader().load_bulk(root_node)
