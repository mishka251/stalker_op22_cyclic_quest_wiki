from typing import TYPE_CHECKING, Generic, TypeVar

from lxml.etree import _Comment

if TYPE_CHECKING:
    from lxml.etree.ElementTree import Element

# pylint: disable=invalid-name
TModel = TypeVar("TModel")


class BaseModelXmlLoader(Generic[TModel]):
    expected_tag: str
    skip_tags: set[str] = set()

    def load(self, root_node: "Element", comments: list[str] | None = None) -> TModel:
        comments = comments or []
        return self._load(root_node, comments)

    def _load(self, root_node: "Element", comments: list[str]) -> TModel:
        raise NotImplementedError

    def load_bulk(self, root_node: "Element") -> list[TModel]:
        comments: list[str] = []
        items = []
        for child_node in root_node:
            if child_node.tag == self.expected_tag:
                item = self.load(child_node, comments)
                items.append(item)
                comments = []
            elif isinstance(child_node, _Comment) and child_node.text:
                comments.append(child_node.text)
            elif child_node.tag in self.skip_tags:
                comments = []
                continue
            else:
                raise ValueError(f"Unexpected node {child_node.tag}")
        return items
