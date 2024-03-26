import logging
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import TextLtxParser
from game_parser.models import SpawnItem, StorylineCharacter, NpcLogicConfig, Trader

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = SpawnItem.objects.count()
        for index, item in enumerate(SpawnItem.objects.all()):
            if item.character_profile_str:
                item.character_profile = (
                        StorylineCharacter.objects.filter(game_id=item.character_profile_str).first()
                        or StorylineCharacter.objects.filter(game_code=item.character_profile_str).first()
                        or StorylineCharacter.objects.filter(name=item.character_profile_str).first()
                )
            if item.custom_data:
                try:
                    info_parser = TextLtxParser(
                        Path(),
                        item.custom_data
                    )
                    custom_data_sections = info_parser.get_parsed_blocks()
                    logic = custom_data_sections.get("logic")
                    if  logic :
                        cfg_file_path = logic.get("cfg")
                        if cfg_file_path:
                            npc_config = NpcLogicConfig.objects.filter(source_file_name=cfg_file_path).first()
                            item.npc_logic = npc_config
                except:
                    pass

            item.save()
            print(f'{index+1:_}/{count:_}')


        count = NpcLogicConfig.objects.count()
        for index, item in enumerate(NpcLogicConfig.objects.all()):
            if item.trade_file_name:
                item.trade_config = Trader.objects.filter(source_file=item.trade_file_name).first()
            item.save()
            print(f'{index + 1:_}/{count:_}')