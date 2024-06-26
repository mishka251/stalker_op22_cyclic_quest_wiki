import logging
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from PIL import Image

from game_parser.models.items.base_item import BaseItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    IMAGE_PART_WIDTH = 50
    IMAGE_PART_HEIGHT = 50

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        base_image_path = (
            settings.OP22_GAME_DATA_PATH / "textures" / "ui" / "ui_icon_equipment.dds"
        )
        image = Image.open(base_image_path)
        count = BaseItem.objects.count()
        for index, item in enumerate(BaseItem.objects.all()):
            logger.debug(f"start {index}/{count} - {item}")
            if not self._item_has_icon(item):
                logger.warning(f"{item} нет данных об иконке")
                continue

            box = self._get_item_image_coordinates(item)
            logger.debug(f"{box=}")
            part = image.crop(box)
            tmp_file_name = Path("tmp.png")
            part.save(tmp_file_name)
            with tmp_file_name.open("rb") as tmp_image:
                item.inv_icon = ImageFile(tmp_image, name=f"{item.name}_icon.png")
                item.save()

            print(f"{index + 1}/{count}")
        image.close()

    def _item_has_icon(self, item: BaseItem) -> bool:
        return (
            item.inv_grid_height is not None
            and item.inv_grid_width is not None
            and item.inv_grid_y is not None
            and item.inv_grid_x is not None
            and item.inv_grid_width > 0
            and item.inv_grid_height > 0
        )

    def _get_item_image_coordinates(self, item: BaseItem) -> tuple[int, int, int, int]:
        inv_grid_x = item.inv_grid_x
        inv_grid_y = item.inv_grid_y

        inv_grid_width = item.inv_grid_width
        inv_grid_height = item.inv_grid_height
        if (
            inv_grid_x is None
            or inv_grid_y is None
            or inv_grid_width is None
            or inv_grid_height is None
        ):
            raise TypeError

        left = inv_grid_x * self.IMAGE_PART_WIDTH
        top = inv_grid_y * self.IMAGE_PART_HEIGHT
        right = (inv_grid_x + inv_grid_width) * self.IMAGE_PART_WIDTH
        bottom = (inv_grid_y + inv_grid_height) * self.IMAGE_PART_HEIGHT

        return (left, top, right, bottom)
