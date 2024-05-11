from pathlib import Path

from django.conf import settings
from django.core.files.images import ImageFile
from lxml.etree import _Comment, _Element
from PIL import Image
from PIL.Image import Image as ImageCls

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import (
    Artefact,
    EncyclopediaArticle,
    EncyclopediaGroup,
    Icon,
    Translation,
)


class EncyclopediaArticleLoader(BaseModelXmlLoader[EncyclopediaArticle]):
    expected_tag = "article"

    def _load(self, article_node: _Element, comments: list[str]) -> EncyclopediaArticle:
        game_id: str | None = article_node.attrib.get("id")
        name: str | None = article_node.attrib.get("name")
        group_name: str | None = article_node.attrib.get("group")
        ltx_str = None
        text: str | None = None
        icon = None
        for child_node in article_node:
            if child_node.tag == "ltx":
                ltx_str = child_node.text
            elif child_node.tag == "text":
                text = child_node.text
            elif child_node.tag == "texture":
                icon = self._parse_icon(child_node)
            elif isinstance(child_node, _Comment):
                pass
            else:
                msg = (
                    f"Unexpected game info_portion child {child_node.tag} in {game_id}"
                )
                raise ValueError(
                    msg,
                )
        if group_name is not None:
            group = EncyclopediaGroup.objects.get_or_create(
                name=group_name,
                defaults={
                    "name_translation": Translation.objects.filter(
                        code=group_name,
                    ).first(),
                },
            )[0]
        else:
            group = None
        artefact = None
        if ltx_str:
            artefact = Artefact.objects.filter(name=ltx_str).first()
        if name is None or text is None or game_id is None:
            raise ValueError
        try:
            article = EncyclopediaArticle.objects.create(
                game_id=game_id,
                name=name,
                name_translation=Translation.objects.filter(code=name).first(),
                group_name=group_name,
                group=group,
                ltx_str=ltx_str,
                icon=icon,
                text=text,
                text_translation=Translation.objects.filter(code=text).first(),
                artefact=artefact,
            )
        except Exception as ex:
            msg = f"{game_id=}, {name=}, {group_name=}"
            raise ValueError(msg) from ex
        return article

    def _parse_icon(self, texture_node: _Element) -> Icon:
        x_ = texture_node.attrib.get("x")
        if texture_node.text is None:
            raise ValueError
        if x_ is None:
            texture_id = texture_node.text
            return Icon.objects.get(name=texture_id)
        x = int(x_)
        y = int(texture_node.attrib.pop("y"))
        width = int(texture_node.attrib.pop("width"))
        height = int(texture_node.attrib.pop("height"))

        image_file = texture_node.text + ".dds"
        base_path = settings.OP22_GAME_DATA_PATH
        texture_id = f"{image_file}_{x}_{y}"
        icon = Icon.objects.filter(name=texture_id).first()
        if icon is not None:
            return icon
        file_path = base_path / "textures" / image_file
        image = Image.open(file_path)
        icon = Icon(name=texture_id)
        self._get_image(image, x, y, width, height, texture_id, icon)
        return icon

    # pylint: disable=too-many-arguments
    def _get_image(
        self,
        image: ImageCls,
        x: int,
        y: int,
        width: int,
        height: int,
        name: str,
        instance: Icon,
    ):
        box = self._get_item_image_coordinates(x, y, width, height)
        part = image.crop(box)
        tmp_file_name = "tmp.png"
        part.save(tmp_file_name)
        with Path(tmp_file_name).open("rb") as tmp_image:
            image_file = ImageFile(tmp_image, name=f"{name}_icon.png")
            instance.icon = image_file
            instance.save()
        return instance

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
