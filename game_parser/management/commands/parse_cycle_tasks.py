from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.ltx_parser import LtxParser
from game_parser.models import CyclicQuest


class Command(BaseCommand):

    def get_file_path(self):
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'misc' / 'cycle_task.ltx'

    _not_quest_keys = {
        'map_locations',
        'vendor',
        'random_0',
        'random_1',
        'random_2',
        'random_3',
        'random_4',
        'random_5',
        'random_6',
        'random_7',
        'random_8'
    }

    @atomic
    def handle(self, **options):
        CyclicQuest.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        quest_blocks = {
            k: v
            for k, v in results.items()
            if k not in self._not_quest_keys
        }

        # print(quest_blocks)
        new_models = []
        existing_models = []
        for quest_name, quest_data in quest_blocks.items():
            model, _new = self._model_from_dict(quest_name, quest_data)
            if _new:
                new_models.append(model)
            else:
                existing_models.append(model)
        CyclicQuest.objects.bulk_create(new_models, batch_size=1_000)
        CyclicQuest.objects.bulk_update(existing_models, batch_size=1_000, fields =[
            'prior',
            'type',
            'target_str',
            'reward_item_string',
            'reward_info_string',
            'random_rewards_string',
        ])

    def _model_from_dict(self, name: str, data: dict[str, str]) -> tuple[CyclicQuest, bool]:
        _new = False
        game_code = name
        giver_code = name[:3]

        quest = CyclicQuest.objects.filter(game_code=game_code, giver_code_local=giver_code).first()
        if quest is None:
            _new = True
            quest = CyclicQuest(game_code=game_code, giver_code_local=giver_code)

        quest.prior = data.pop('prior') if 'prior' in data else 0
        quest.type = data.pop('type')
        quest.target_str = data.pop('target')
        if 'reward_item' in data:
            quest.reward_item_string = data.pop('reward_item')
        if 'reward_info' in data:
            quest.reward_info_string = data.pop('reward_info')
        if 'reward_random' in data:
            quest.random_rewards_string = data.pop('reward_random')
        if 'once' in data:
            quest.once = (data.pop('once') == 'true')
        if 'target_cond' in data:
            quest.target_cond_str = data.pop('target_cond')
        if 'map_location' in data:
            quest.map_location = data.pop('map_location')
        if 'reward_money' in data:
            quest.reward_money = data.pop('reward_money')
        if 'target_count' in data:
            quest.target_count = data.pop('target_count')
        if 'condlist' in data:
            quest.condlist_str = data.pop('condlist')
        if 'hide_reward' in data:
            quest.once = (data.pop('hide_reward') == 'true')
        if 'reward_treasure' in data:
            quest.once = (data.pop('reward_treasure') == 'true')
        if 'reward_relation' in data:
            quest.reward_relation_str = data.pop('reward_relation')
        if 'defend_target' in data:
            quest.defend_target_str = data.pop('defend_target')
        if 'reward_dialog' in data:
            quest.reward_dialog_str = data.pop('reward_dialog')
        if data:
            print('unused_data', data)
        return quest, _new
