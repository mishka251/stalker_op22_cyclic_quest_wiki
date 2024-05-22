import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CustomSpawnItem, NpcLogicConfig, StorylineCharacter

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = CustomSpawnItem.objects.count()
        for index, item in enumerate(CustomSpawnItem.objects.all()):
            if item.character_profile_str:
                item.character_profile = StorylineCharacter.objects.filter(
                    game_id=item.character_profile_str,
                ).first()
            if item.custom_data:
                item.npc_logic = NpcLogicConfig.objects.filter(
                    source_file_name=item.custom_data,
                ).first()
            item.save()
            print(f"{index + 1}/{count}")
