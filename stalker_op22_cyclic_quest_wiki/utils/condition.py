import dataclasses


@dataclasses.dataclass
class ItemCondition:
    min: float
    max: float

    def to_json(self) -> dict:
        return {
            "min": self.min,
            "max": self.max,
        }
