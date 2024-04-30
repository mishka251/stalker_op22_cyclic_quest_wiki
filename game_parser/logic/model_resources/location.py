from game_parser.logic.model_resources.base_resource import SECTION_NAME, BaseModelResource, CharField
from game_parser.models import Location


class LocationResource(BaseModelResource):
    _model_cls = Location
    _fields = [
        CharField(SECTION_NAME, "game_code"),
        CharField("id", "game_id"),
        CharField("name"),
        CharField("offset", "offset_str"),
    ]

    _exclude_fields = {
        "caption",
    }
