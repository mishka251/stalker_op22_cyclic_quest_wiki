import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import Anomaly, EncyclopediaArticle

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / "misc" / 'zones.ltx'

    @atomic
    def handle(self, **options):
        Anomaly.objects.all().delete()

        known_bases = {
            "anomaly": {
                "is_anomaly": True,
            }
        }

        parser = LtxParser(self.get_file_path(), known_extends=known_bases)
        results = parser.get_parsed_blocks()

        blocks = {
            k: v
            for k, v in results.items()
            if v.get("is_anomaly", False)
        }

        for quest_name, quest_data in blocks.items():
            print(quest_name)
            Anomaly.objects.create(
                section_name=quest_name,
                class_name=quest_data.get("class"),
                visual_str=quest_data.get("visual"),
                hit_type=quest_data.get("hit_type"),
                article=EncyclopediaArticle.objects.filter(game_id=quest_name).first(),
            )