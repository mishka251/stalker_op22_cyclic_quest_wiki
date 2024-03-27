import re

from django.views.generic import TemplateView
from django.db.models.functions import Lower

from game_parser.logic.tasks_grouping import collect_info
from game_parser.models import SpawnItem, Location, LocationMapInfo, CycleTaskVendor
from game_parser.models.quest import QuestKinds


class TasksListView(TemplateView):

    template_name = 'vendors_tasks_list.html'

    def get_context_data(self, **kwargs):
        data = collect_info()
        return {'vendors_quests': data}


class EscapeMap(TemplateView):
    template_name = "escape_map.html"
    location_name = "L01_escape"

    def get_context_data(self, **kwargs):
        location_name = kwargs.get("location", self.location_name)
        location = Location.objects.annotate(name_lowe=Lower("name")).get(name_lowe=location_name.lower())
        spawn_items = SpawnItem.objects.filter(location=location)
        location_info = LocationMapInfo.objects.get(location=location)
        offset_re = re.compile(r"\s*(?P<min_x>.*),\s*(?P<min_y>.*),\s*(?P<max_x>.*),\s*(?P<max_y>.*)")
        rm = offset_re.match(location_info.bound_rect_raw)
        (min_x, min_y, max_x, max_y) = (
            float(rm.group("min_x")),
            float(rm.group("min_y")),
            float(rm.group("max_x")),
            float(rm.group("max_y"))
        )

        y_level_offset = -(max_y + min_y)
        return {
            "layer_image_url": location_info.map_image.url,
            "map_size": (location_info.map_image.width, location_info.map_image.height),
            "map_offset": (min_x, min_y, max_x, max_y),
            "items": [self._spawn_item_to_dict(item) for item in spawn_items],
            "y_level_offset": y_level_offset,
        }

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


class TaskVendorsList(TemplateView):
    template_name = "task_vendors_list/task_vendor_list.html"

    def get_context_data(self, **kwargs):
        vendors = CycleTaskVendor.objects.all()
        return {
            "vendors": [self._vendor_to_dict(vendor) for vendor in vendors]
        }

    def _vendor_to_dict(self, vendor: CycleTaskVendor) -> dict:
        npc_profile = vendor.get_npc_profile()
        return {
            "image_path": self._get_npc_profile_icon(npc_profile) if npc_profile else None,
            "name": npc_profile.name_translation.rus if npc_profile and npc_profile.name_translation else None,
            "tasks_count": vendor.cyclicquest_set.count(),
            "has_chain": vendor.cyclicquest_set.filter(type=QuestKinds.chain).exists(),
            "quests_link": "",
        }

    def _get_npc_profile_icon(self, npc_profile):
        return npc_profile.icon and npc_profile.icon.icon and npc_profile.icon.icon.url