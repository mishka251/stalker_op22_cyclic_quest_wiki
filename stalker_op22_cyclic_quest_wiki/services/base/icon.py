import dataclasses

from stalker_op22_cyclic_quest_wiki.models import Icon


@dataclasses.dataclass
class IconData:
    url: str
    width: int
    height: int

    def to_json(self) -> dict:
        return {
            "url": self.url,
            "width": self.width,
            "height": self.height,
        }

    @classmethod
    def from_icon(cls, icon: Icon) -> "IconData":
        return cls(
            icon.icon.url,
            icon.icon.width,
            icon.icon.height,
        )
