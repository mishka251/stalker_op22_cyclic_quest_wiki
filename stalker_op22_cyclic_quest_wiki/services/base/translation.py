import dataclasses

from stalker_op22_cyclic_quest_wiki.models import Translation


@dataclasses.dataclass
class TranslationData:
    rus: str
    eng: str
    ukr: str
    pln: str
    fra: str

    def to_json(self) -> dict:
        return {
            "rus": self.rus,
            "eng": self.eng,
            "ukr": self.ukr,
            "pln": self.pln,
            "fra": self.fra,
        }

    @classmethod
    def from_translation(cls, translation: Translation) -> "TranslationData":
        return cls(
            rus=translation.rus,
            eng=translation.eng,
            ukr=translation.ukr,
            pln=translation.pln,
            fra=translation.fra,
        )
