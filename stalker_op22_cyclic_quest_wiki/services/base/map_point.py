import dataclasses


@dataclasses.dataclass
class MapPointItem:
    position: tuple[float, float]
    info_str: str


@dataclasses.dataclass
class MapPointInfo:
    unique_map_id: str
    image_url: str
    bounds: tuple[float, float, float, float]
    item: MapPointItem
    y_level_offset: float

    def to_json(self) -> dict:
        return {
            "image_url": self.image_url,
            "bounds": list(self.bounds),
            "y_level_offset": self.y_level_offset,
            "position": self.item.position,
            "caption": self.item.info_str,
        }
