import re
from decimal import Decimal
from typing import Optional, Iterable

from django.template import loader
from django.db.models import Model
from django.contrib.admin import ModelAdmin, register, display, TabularInline
from django.utils.safestring import mark_safe

from game_parser.models import ItemReward, SpawnReward, CyclicQuest, ItemInSell, ItemInBuy, QuestRandomReward, \
    ItemInTreasure, SpawnItem, Recept, LocationMapInfo
from game_parser.models.items.base_item import BaseItem
from game_parser.models.quest import CyclicQuestItemReward
from game_parser.utils.admin_utils.icon_view import icon_view
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class SpawnItemMapRenderer:
    def __init__(self, item: SpawnItem):
        self._item = item

    def render(self) -> Optional[str]:
        return self._map(self._item)

    def _get_location_map(self, obj: SpawnItem) -> "Optional[LocationMapInfo]":
        if not obj.location:
            return None
        location_info = obj.location.locationmapinfo_set.first()
        return location_info


    def _map(self, obj: SpawnItem) -> Optional[str]:
        location = obj.location
        location_info = LocationMapInfo.objects.get(location=location)
        if not location_info.bound_rect_raw or not location_info.map_image:
            return None
        offset_re = re.compile(r"\s*(?P<min_x>.*),\s*(?P<min_y>.*),\s*(?P<max_x>.*),\s*(?P<max_y>.*)")
        rm = offset_re.match(location_info.bound_rect_raw)
        (min_x, min_y, max_x, max_y) = (
            float(rm.group("min_x")),
            float(rm.group("min_y")),
            float(rm.group("max_x")),
            float(rm.group("max_y"))
        )

        y_level_offset = -(max_y + min_y)
        context = {
            "item": self._spawn_item_to_dict(obj),
            "item_var_name": f"item_{obj.id}",
            "map_offset": (min_x, min_y, max_x, max_y),
            "map_offset_name": f"map_offset_{obj.id}",
            "y_level_offset": y_level_offset,
            "y_level_offset_name": f"y_level_offset_{obj.id}",
            "layer_image_url": location_info.map_image.url,
            "item_id": str(obj.id),
        }
        return loader.render_to_string("leaflet_map_field.html", context)

    def _spawn_item_to_dict(self, spawn_item: SpawnItem) -> dict:
        position_re = re.compile(r"\s*(?P<x>.*),\s*(?P<y>.*),\s*(?P<z>.*)")
        rm = position_re.match(spawn_item.position_raw)
        if not rm:
            return None
        (x, y, z) = float(rm.group("x")), float(rm.group("y")), float(rm.group("z"))
        position = (x, z)
        name = spawn_item.name
        section_name = spawn_item.section_name

        return {
            "position": position,
            "name": name,
            "section_name": section_name,
        }

def _item_link(item: Model) -> str:
    href = f"/admin/{item._meta.app_label}/{item._meta.model_name}/{item.pk}"
    str_ = str(item)
    return f"<a href='{href}'> {str_} </a>"

def links_list(items: Iterable[Model]) -> str:
    return "\n".join(map(_item_link, items))