import logging
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from lxml.etree import parse, Element

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.logic.model_xml_loaders.encyclopedia import EncyclopediaArticleLoader
from game_parser.models import EncyclopediaGroup, EncyclopediaArticle, Translation, Icon, Artefact

from pathlib import Path
# from xml.etree.ElementTree import Element, parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from lxml.etree import parse, Element, _Comment

from game_parser.models import GameTask, TaskObjective, MapLocationType, Dialog, Icon
from game_parser.models.game_story.dialog import DialogPhrase
from PIL import Image
from django.core.files.images import ImageFile


logger = logging.getLogger(__name__)
DEFAULT_ENCODING = "windows-1251"

class Command(BaseCommand):
    TMP_DIR = Path('tmp')

    def get_file_path(self):
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'gameplay' / 'encyclopedia.xml'

    @atomic
    def handle(self, **options):
        EncyclopediaGroup.objects.all().delete()
        EncyclopediaArticle.objects.all().delete()
        fixer = GSCXmlFixer(self.get_file_path())
        fixed_file_path = fixer.fix()
        root_node = parse(fixed_file_path).getroot()
        EncyclopediaArticleLoader().load_bulk(root_node)

