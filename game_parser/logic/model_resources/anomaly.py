from typing import Any

from game_parser.logic.model_resources.base_resource import BaseModelResource, SECTION_NAME, CharField
from game_parser.models import Anomaly, EncyclopediaArticle


class AnomalyResource(BaseModelResource):
    _model_cls = Anomaly
    _fields = [
        CharField(SECTION_NAME, 'name'),
        CharField("class", 'class_name', required=False),
        CharField("visual", 'visual_str', required=False),
        CharField("hit_type", 'hit_type', required=False),
    ]

    def _apply_data(self, data: dict[str, Any], instance: Anomaly):
        super()._apply_data(data, instance)
        instance.article = EncyclopediaArticle.objects.filter(game_id=instance.section_name).first()
