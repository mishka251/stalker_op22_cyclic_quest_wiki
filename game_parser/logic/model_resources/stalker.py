from game_parser.logic.model_resources.base_resource import (
    SECTION_NAME,
    BaseModelResource,
    CharField,
)
from game_parser.models import StalkerSection


class StalkerResource(BaseModelResource):
    _model_cls = StalkerSection
    _fields = [
        CharField(SECTION_NAME, "section_name"),
        CharField("character_profile", "character_profile_str", required=False),
        CharField("spec_rank", "spec_rank_str", required=False),
        CharField("community", "community_str", required=False),
        CharField("custom_data", "custom_data_path", required=False),
    ]
