from django.template import Library
from django.template.loader import render_to_string

from game_parser.logic.tasks_grouping import MapPointInfo

register = Library()


@register.simple_tag
def render_map_item(
    map_item_info: MapPointInfo,
    map_id: str,
    index: str | None = None,
) -> str:
    if index is not None:
        map_id = f"{map_id}_{index}"
    template_name = "leaflet_map_field.html"
    context = {
        "item": {
            "position": map_item_info.item.position,
            "info_str": map_item_info.item.info_str,
        },
        "item_var_name": f"{map_id}_item",
        "map_offset": map_item_info.bounds,
        "map_offset_name": f"{map_id}_offset",
        "y_level_offset": map_item_info.y_level_offset,
        "y_level_offset_name": f"{map_id}_offset_y",
        "layer_image_url": map_item_info.image_url,
        "item_id": map_id,
    }
    return render_to_string(template_name, context)
