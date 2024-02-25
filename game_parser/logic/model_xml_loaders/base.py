from typing import Generic, TypeVar, Optional

from lxml.etree import Element, _Comment

TModel = TypeVar("TModel")


class BaseModelXmlLoader(Generic[TModel]):
    expected_tag: str
    skip_tags = set()

    def load(self, root_node: Element, comments: Optional[list[str]]=None) -> TModel:
        comments = comments or []
        return self._load(root_node, comments)

    def _load(self, root_node: Element, comments: list[str]) -> TModel:
        raise NotImplementedError()

    def load_bulk(self, root_node: Element) -> list[TModel]:
        comments = []
        items = []
        for child_node in root_node:
            if child_node.tag == self.expected_tag:
                item = self.load(child_node, comments)
                items.append(item)
                comments = []
            elif isinstance(child_node, _Comment):
                comments.append(child_node.text)
            elif child_node.tag in self.skip_tags:
                comments = []
                continue
            else:
                raise ValueError(f'Unexpected node {child_node.tag}')
        return items
