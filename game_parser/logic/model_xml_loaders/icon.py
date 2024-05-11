from pathlib import Path

from django.core.files.images import ImageFile
from lxml.etree import _Element
from PIL.Image import Image as ImageCls

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import Icon


class IconLoader(BaseModelXmlLoader[Icon]):
    expected_tag = "texture"
    skip_tags = {
        "file_name",
    }

    def __init__(self, image: ImageCls):
        self.image = image

    def _load(self, texture_node: _Element, comments: list[str]) -> Icon:
        if texture_node.tag != "texture":
            msg = f"Unexpected node {texture_node.tag}"
            raise ValueError(msg)

        texture_id = texture_node.attrib.pop("id")
        if not isinstance(texture_id, str):
            raise TypeError
        x = int(texture_node.attrib.pop("x"))
        y = int(texture_node.attrib.pop("y"))
        width = int(texture_node.attrib.pop("width"))
        height = int(texture_node.attrib.pop("height"))
        icon = Icon(name=texture_id)
        self._get_image(x, y, width, height, texture_id, icon)
        return icon

    def _get_item_image_coordinates(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> tuple[int, int, int, int]:
        inv_grid_x = x
        inv_grid_y = y

        inv_grid_width = width
        inv_grid_height = height

        left = inv_grid_x  # * self.IMAGE_PART_WIDTH
        top = inv_grid_y  # * self.IMAGE_PART_HEIGHT
        right = inv_grid_x + inv_grid_width  # * self.IMAGE_PART_WIDTH
        bottom = inv_grid_y + inv_grid_height  # * self.IMAGE_PART_HEIGHT

        return (left, top, right, bottom)

    # pylint: disable=too-many-arguments
    def _get_image(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        name: str,
        instance: Icon,
    ) -> None:
        box = self._get_item_image_coordinates(x, y, width, height)
        part = self.image.crop(box)
        tmp_file_name = Path("tmp.png")
        part.save(tmp_file_name)
        with tmp_file_name.open("rb") as tmp_image:
            image_file = ImageFile(tmp_image, name=f"{name}_icon.png")
            instance.icon = image_file
            instance.save()
