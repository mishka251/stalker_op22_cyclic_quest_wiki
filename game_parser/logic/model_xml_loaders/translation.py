import logging

from lxml.etree import _Element

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import Translation

logger = logging.getLogger(__name__)

class TranslationLoader(BaseModelXmlLoader[Translation]):
    expected_tag = "string"

    def _load(self, character_node: _Element, comments: list[str]) -> Translation:
        if character_node.tag != "string":
            logger.warning(f"wrong child  {character_node}, {character_node}")
            raise ValueError(f"wrong child  {character_node}, {character_node}")
        code = character_node.attrib["id"]
        kwargs = {}
        for sub_child in character_node:
            kwargs[sub_child.tag] = sub_child.text
        translation = Translation(code=code, **kwargs)
        translation.save()
        # print(translation)
        return translation
