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
    def handle(self, *args, **options):
        for reward in QuestRandomReward.objects.all():
            self._set_reward_icon(reward)
            reward.save()

    def _set_reward_icon(self, reward: QuestRandomReward) -> None:
        name = f"random_{reward.index}"
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