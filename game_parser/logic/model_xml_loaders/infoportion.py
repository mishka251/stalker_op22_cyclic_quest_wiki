import logging

from lxml.etree import _Comment, _Element

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import InfoPortion

logger = logging.getLogger(__name__)


class InfoPortionLoader(BaseModelXmlLoader[InfoPortion]):
    expected_tag = "info_portion"

    def _load(self, root_node: _Element, comments: list[str]) -> InfoPortion:
        info_portion_id = root_node.attrib.pop("id")
        if not isinstance(info_portion_id, str):
            raise TypeError
        info_portion = InfoPortion.objects.create(game_id=info_portion_id)
        article_raw = []
        disable_raw = []
        task_raw = []
        actions_raw = []
        for child_node in root_node:
            if child_node.tag == "article" and child_node.text is not None:
                article_raw.append(child_node.text)
            elif child_node.tag == "disable" and child_node.text is not None:
                disable_raw.append(child_node.text)
            elif child_node.tag == "task" and child_node.text is not None:
                task_raw.append(child_node.text)
            elif child_node.tag == "action" and child_node.text is not None:
                actions_raw.append(child_node.text)
            elif isinstance(child_node, _Comment):
                pass
            else:
                logger.warning(
                    "Unexpected game info_portion child %s in %s",
                    child_node.tag,
                    info_portion_id,
                )
        info_portion.article_raw = ";".join(article_raw)
        info_portion.disable_raw = ";".join(disable_raw)
        info_portion.task_raw = ";".join(task_raw)
        info_portion.actions_raw = ";".join(actions_raw)
        info_portion.save()
        return info_portion
