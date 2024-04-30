import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.encyclopedia import EncyclopediaArticleLoader
from game_parser.models import EncyclopediaArticle, EncyclopediaGroup

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    TMP_DIR = Path("tmp")

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "gameplay" / "encyclopedia.xml"

    @atomic
    def handle(self, **options) -> None:
        EncyclopediaGroup.objects.all().delete()
        EncyclopediaArticle.objects.all().delete()
        fixer = GSCXmlFixer()
        fixed_file_path = fixer.fix(self.get_file_path())
        root_node = parse(fixed_file_path).getroot()
        EncyclopediaArticleLoader().load_bulk(root_node)
