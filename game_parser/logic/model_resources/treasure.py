from game_parser.logic.model_resources.base_resource import BaseModelResource, SECTION_NAME, CharField
from game_parser.models import Treasure


class TreasureResource(BaseModelResource):
    _model_cls = Treasure
    _fields = [
        CharField(SECTION_NAME, 'name_str'),
        CharField('target'),
        CharField('condlist', 'condlist_str'),
        CharField('description', 'description_str'),
        CharField('items', 'items_str'),
        CharField('name', 'custom_name', required=False),
    ]

    _exclude_fields = {
        'named',
    }
