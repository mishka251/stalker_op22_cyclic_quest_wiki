import logging

from lxml.etree import Element, _Comment

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import InfoPortion

logger = logging.getLogger(__name__)


class InfoPortionLoader(BaseModelXmlLoader[InfoPortion]):
    expected_tag = "info_portion"

    def _load(self, root_node: Element, comments: list[str]) -> InfoPortion:
        info_portion_id = root_node.attrib.pop("id", None)
        info_portion = InfoPortion.objects.create(game_id=info_portion_id)
        article_raw = []
        disable_raw = []
        task_raw = []
        actions_raw = []
        for child_node in root_node:
            if child_node.tag == "article":
                article_raw.append(child_node.text)
            elif child_node.tag == "disable":
                disable_raw.append(child_node.text)
            elif child_node.tag == "task":
                task_raw.append(child_node.text)
            elif child_node.tag == "action":
                actions_raw.append(child_node.text)
            elif isinstance(child_node, _Comment):
                pass
            else:
                logger.warning(
                    f"Unexpected game info_portion child {child_node.tag} in {info_portion_id}"
                )
        info_portion.article_raw = ";".join(article_raw)
        info_portion.disable_raw = ";".join(disable_raw)
        info_portion.task_raw = ";".join(task_raw)
        info_portion.actions_raw = ";".join(actions_raw)
        info_portion.save()
        return info_portion
