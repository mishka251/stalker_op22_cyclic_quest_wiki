import logging
from pathlib import Path
from typing import Mapping, Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser, KnownExtendsType
from game_parser.logic.model_resources.anomaly import AnomalyResource
from game_parser.models import Anomaly

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "misc" / "zones.ltx"

    @atomic
    def handle(self, **options) -> None:
        Anomaly.objects.all().delete()

        known_bases: KnownExtendsType = {
            "anomaly": {
                "is_anomaly": "True",
            },
        }

        parser = LtxParser(self.get_file_path(), known_extends=known_bases)
        results = parser.get_parsed_blocks()

        blocks: dict[str, dict] = {
            k: v
            for k, v in results.items()
            if isinstance(v, dict) and v.get("is_anomaly", False) == "True"
        }

        for quest_name, quest_data in blocks.items():
            print(quest_name)
            AnomalyResource().create_instance_from_data(quest_name, quest_data)
