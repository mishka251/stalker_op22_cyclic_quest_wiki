from pathlib import Path

from PIL import Image
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import CyclicQuest, QuestRandomReward, Translation
from game_parser.models import Icon


# from xml.etree.ElementTree import Element, parse


class Command(BaseCommand):

    def get_file_path(self):
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config' / 'misc' / 'cycle_task.ltx'

    _not_quest_keys = {
        'map_locations',
        'vendor',
    }

    _random_rewards_keys = {
        'random_0',
        'random_1',
        'random_2',
        'random_3',
        'random_4',
        'random_5',
        'random_6',
        'random_7',
        'random_8',
    }

    @atomic
    def handle(self, **options):
        CyclicQuest.objects.all().delete()
        QuestRandomReward.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        quest_blocks = {
            k: v
            for k, v in results.items()
            if k not in self._not_quest_keys
        }

        for quest_name, quest_data in quest_blocks.items():
            if quest_name in self._random_rewards_keys:
                model = self._create_random_reward(quest_name, quest_data)
            else:
                model = self._model_from_dict(quest_name, quest_data)
            model.save()


    def _model_from_dict(self, name: str, data: dict[str, str]) -> CyclicQuest:
        game_code = name
        giver_code = name[:3]

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
            quest.hide_reward = (data.pop('hide_reward') == 'true')
        if 'reward_treasure' in data:
            quest.reward_treasure = (data.pop('reward_treasure') == 'true')
        if 'reward_relation' in data:
            quest.reward_relation_str = data.pop('reward_relation')
        if 'defend_target' in data:
            quest.defend_target_str = data.pop('defend_target')
        if 'reward_dialog' in data:
            quest.reward_dialog_str = data.pop('reward_dialog')
        if data:
            print('unused_data', data)
        return quest

    def _create_random_reward(self, name: str, data: list[str]) -> QuestRandomReward:
        possible_items_str = ';'.join(data)
        reward =  QuestRandomReward(name=name, possible_items_str=possible_items_str)
        self._set_reward_icon(reward)
        self._set_reward_translation(reward)
        return reward

    def _set_reward_translation(self, reward: QuestRandomReward) -> None:
        name = reward.name
        prefix = "random_"
        index_str = name[len(prefix):]
        index = int(index_str)
        translation_prefix = "task_item_type_"
        translation = Translation.objects.filter(code=f"{translation_prefix}{index}").first()
        reward.name_translation = translation
        reward.index = index

    def _set_reward_icon(self, reward: QuestRandomReward) -> None:
        name = reward.name
        tips_icons = {
            "random_0": [1700, 4000],
            "random_1": [1600, 4000],
            "random_2": [1800, 4000],
            "random_3": [1900, 4000],
            "random_4": [1300, 4000],
            "random_5": [2000, 4000],
            "random_6": [1200, 4000],
            "random_7": [1500, 4000],
            "random_8": [1400, 4000],
        }
        (icon_left, icon_top) = tips_icons[name]
        icon_w = 100
        icon_h = 50
        icon_file: Path = settings.OP22_GAME_DATA_PATH/"textures"/"ui"/"ui_icon_equipment.dds"
        image = Image.open(icon_file)
        icon = self._get_image(image, icon_left, icon_top, icon_w, icon_h, name)
        reward.icon = icon

    def _get_image(self, image: Image, x: int, y: int, width: int, height: int, name: str) -> Icon:
        instance: Icon = Icon(name=name)
        box = self._get_item_image_coordinates(x, y, width, height)
        # logger.debug(f'{box=}')
        part = image.crop(box)
        tmp_file_name = 'tmp.png'
        part.save(tmp_file_name)
        with open(tmp_file_name, 'rb') as tmp_image:
            image_file = ImageFile(tmp_image, name=f'{name}_icon.png')
            instance.icon = image_file
            instance.save()
        return instance

    def _get_item_image_coordinates(self, x: int, y: int, width: int, height: int) -> tuple[int, int, int, int]:
        inv_grid_x = x
        inv_grid_y = y

        inv_grid_width = width
        inv_grid_height = height

        left = inv_grid_x  # * self.IMAGE_PART_WIDTH
        top = inv_grid_y  # * self.IMAGE_PART_HEIGHT
        right = (inv_grid_x + inv_grid_width)  # * self.IMAGE_PART_WIDTH
        bottom = (inv_grid_y + inv_grid_height)  # * self.IMAGE_PART_HEIGHT

        return (left, top, right, bottom)