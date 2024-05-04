import logging
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import TextLtxParser
from game_parser.models import NpcLogicConfig, SpawnItem, StorylineCharacter, Trader

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        count = SpawnItem.objects.count()
        for index, spawn_item in enumerate(SpawnItem.objects.all()):
            if spawn_item.character_profile_str:
                spawn_item.character_profile = (
                    StorylineCharacter.objects.filter(
                        game_id=spawn_item.character_profile_str,
                    ).first()
                    or StorylineCharacter.objects.filter(
                        game_code=spawn_item.character_profile_str,
                    ).first()
                    or StorylineCharacter.objects.filter(
                        name=spawn_item.character_profile_str,
                    ).first()
                )
            if spawn_item.custom_data:
                try:
                    spawn_item.npc_logic = self.parse_custom_data(spawn_item)
                except Exception:
                    logger.exception(f"{spawn_item.custom_data}")

            spawn_item.save()
            print(f"{index+1:_}/{count:_}")

        count = NpcLogicConfig.objects.count()
        for index, npc_logic in enumerate(NpcLogicConfig.objects.all()):
            if npc_logic.trade_file_name:
                npc_logic.trade_config = Trader.objects.filter(
                    source_file=npc_logic.trade_file_name,
                ).first()
            npc_logic.save()
            print(f"{index + 1:_}/{count:_}")

    def parse_custom_data(self, spawn_item) -> NpcLogicConfig | None:
        info_parser = TextLtxParser(
            Path(),
            spawn_item.custom_data,
        )
        custom_data_sections = info_parser.get_parsed_blocks()
        logic = custom_data_sections.get("logic")
        if logic:
            if not isinstance(logic, dict):
                raise TypeError
            cfg_file_path = logic.get("cfg")
            if cfg_file_path:
                return NpcLogicConfig.objects.filter(
                    source_file_name=cfg_file_path,
                ).first()
        return None
