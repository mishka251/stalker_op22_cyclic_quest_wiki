from game_parser.logic.model_resources.base_resource import BaseModelResource, SECTION_NAME, CharField, IntegerField
from game_parser.models import Monster


class MonsterResource(BaseModelResource):
    _model_cls = Monster
    _fields = [
        CharField(SECTION_NAME, 'section_name'),
        CharField("short_name", 'short_name', required=False),
        CharField('visual', 'visual_str', required=False, default=None),
        CharField('corpse_visual', 'corpse_visual_str', required=False, default=None),
        CharField('icon', 'icon_str', required=False, default=None),
        CharField('Spawn_Inventory_Item_Section', 'Spawn_Inventory_Item_Section', required=False, default=None),
        CharField('Spawn_Inventory_Item_Probability', 'Spawn_Inventory_Item_Probability', required=False, default=None),
        CharField('class', 'class_name', required=False, default=None),
        CharField('terrain', 'terrain', required=False, default=None),
        CharField('species', 'species', required=False, default=None),
        CharField('spec_rank', 'spec_rank', required=False, default=None),
    ]
