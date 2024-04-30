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
        return base_path / "config"/"gameplay"

    def get_files_paths(self, path: Path) -> list[Path]:
        paths = []
        for path in path.iterdir():
            if path.name.startswith("tasks"):
                paths.append(path)
        # for (dir, _, files) in os.walk(path):
        #     for file_name in files:
        #         paths.append(Path(os.path.join(dir, file_name)))

        return paths

    @atomic
    def handle(self, **options):
        GameTask.objects.all().delete()
        TaskObjective.objects.all().delete()

        for file_path in self.get_files_paths(self.get_files_dir_path()):
            print(file_path)
            fixer = GSCXmlFixer()
            fixed_file_path = fixer.fix(file_path)
            with open(fixed_file_path, "r") as tml_file:
                root_node = parse(tml_file).getroot()
            # print(root_node)
            GameTaskLoader().load_bulk(root_node)
