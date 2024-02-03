import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.logic.model_resources.base_item import MonsterPartResource, OutfitResource
from game_parser.models import MonsterPart, Outfit, Monster

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self):
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'creatures' / 'monsters.ltx'

    # _exclude_keys = {
    #     'without_outfit',
    #     'nano_resistance',
    #     'sect_mil_exoskeleton',
    #     'sect_mil_exoskeleton_add',
    #     'sect_mil_exoskeleton_adr',
    # }

    @atomic
    def handle(self, **options):
        Monster.objects.all().delete()

        known_bases = {
            "base": {},
            'monster': {
                "monster": "true",
            },
        }

        parser = LtxParser(self.get_file_path(), known_extends=known_bases)
        results = parser.get_parsed_blocks()

        quest_blocks = {
            k: v
            for k, v in results.items()
            if isinstance(v, dict) and v.get("monster", "false") == "true"
            # if k not in self._exclude_keys and not k.endswith('immunities')
        }

        # resource = OutfitResource()

        for quest_name, quest_data in quest_blocks.items():
            print(quest_name)
            monster = Monster.objects.create(
                section_name=quest_name,
                short_name=quest_data.get("short_name"),
                visual_str=quest_data.get("visual"),
                corpse_visual_str=quest_data.get("corpse_visual"),
                icon_str=quest_data.get("icon"),
                Spawn_Inventory_Item_Section=quest_data.get("Spawn_Inventory_Item_Section"),
                Spawn_Inventory_Item_Probability=quest_data.get("Spawn_Inventory_Item_Probability"),
                class_name=quest_data.get("class"),
                terrain=quest_data.get("terrain"),
                species=quest_data.get("species"),
                spec_rank=quest_data.get("spec_rank"),
            )
            # item = resource.create_instance_from_data(quest_name, quest_data)
            # if quest_data:
            #     logger.warning(f'unused data {quest_data} in {quest_name}')
