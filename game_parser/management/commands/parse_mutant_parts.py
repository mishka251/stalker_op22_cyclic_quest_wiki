from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.ltx_parser import LtxParser
from game_parser.models import MonsterPart


class Command(BaseCommand):

    def get_file_path(self):
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'misc' / 'monster_items.ltx'

    _exclude_keys = {
        'monster_part'
    }

    @atomic
    def handle(self, **options):
        MonsterPart.objects.all().delete()

        known_bases = {
            'II_ATTCH': {},
        }

        parser = LtxParser(self.get_file_path(), known_extends=known_bases)
        results = parser.get_parsed_blocks()

        quest_blocks = {
            k: v
            for k, v in results.items()
            if k not in self._exclude_keys
        }

        for quest_name, quest_data in quest_blocks.items():
            print(quest_name)
            model = self._mutant_part_from_dict(quest_name, quest_data)
            if quest_data:
                print('unused data', quest_data)
            model.save()

    def _mutant_part_from_dict(self, name: str, data: dict[str, str]) -> MonsterPart:
        ammo = MonsterPart(
            name=name,
            visual_str=data.pop('visual'),
            description_code=data.pop('description'),
            cost=int(data.pop('cost')),
            inv_name=data.pop('inv_name'),
            inv_name_short=data.pop('inv_name_short', None),
            inv_weight=Decimal(data.pop('inv_weight')),
            quest_item=data.pop('quest_item', 'false') == 'true',
        )
        return ammo
