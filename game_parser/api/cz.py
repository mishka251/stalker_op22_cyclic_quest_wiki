import re

from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.views.generic import View

from game_parser.models import (
    BaseItem,
    CycleTaskVendor,
    CyclicQuest,
    LocationMapInfo,
    QuestRandomReward,
    SpawnItem,
    Translation,
)
from game_parser.models.quest import CyclicQuestItemReward, QuestRandomRewardThrough


class QuestGiversView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        quest_givers = CycleTaskVendor.objects.all()

        results = []
        for quest_giver in quest_givers:
            npc_profile = quest_giver.get_npc_profile()
            if npc_profile is None:
                raise ValueError("No npc_profile")
            name_translations = npc_profile.name_translation
            quest_giver_json = {
                "id": str(quest_giver.id),
                "name": (
                    {
                        "rus": name_translations.rus,
                        "eng": name_translations.eng,
                        "ukr": name_translations.ukr,
                        "pln": name_translations.pln,
                        "fra": name_translations.fra,
                    }
                    if name_translations is not None
                    else None
                ),
                "icon_url": (
                    npc_profile.icon.icon.url if npc_profile.icon is not None else None
                ),
            }
            results.append(quest_giver_json)
        return JsonResponse(results, safe=False)


class VendorCyclicQuests(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        vendor_id = request.GET["vendor_id"]
        vendor = CycleTaskVendor.objects.get(id=vendor_id)
        quests: list[CyclicQuest] = list(CyclicQuest.objects.filter(vendor=vendor))
        results = []
        for quest in quests:
            quest_giver_json = {
                "type": quest.type,
                "prior": quest.prior,
                "rewards": {
                    "items": [
                        self._reward_item_to_json(item)
                        for item in quest.item_rewards.all()
                    ],
                    "money": quest.reward_money,
                    "treasure": quest.reward_treasure,
                    "relation": quest.reward_relation_str,
                    "random": [
                        self._random_reward_to_json(item)
                        for item in quest.random_rewards.all()
                    ],
                },
                "targets": {
                    "item": (
                        {
                            "item": self._item_to_json(quest.target_item),
                            "count": quest.target_count,
                        }
                        if quest.target_item is not None
                        else None
                    ),
                    "camp_destroy": (
                        self._camp_to_dict(quest.target_camp_to_destroy)
                        if quest.target_camp_to_destroy is not None
                        else None
                    ),
                    "camp_defeat": (
                        self._camp_to_dict(quest.target_camp_to_defeat)
                        if quest.target_camp_to_defeat is not None
                        else None
                    ),
                },
                "once": quest.once,
                "hide_reward": quest.hide_reward,
            }
            results.append(quest_giver_json)
        return JsonResponse(results, safe=False)

    def _reward_item_to_json(self, reward_item: CyclicQuestItemReward) -> dict:
        if reward_item.item is None:
            raise ValueError
        return {
            "count": reward_item.count,
            "item": self._item_to_json(reward_item.item),
        }

    def _item_to_json(self, item: BaseItem) -> dict:
        return {
            "name": item.name,
            "icon_url": item.inv_icon.url,
            "description": (
                {
                    "rus": item.description_translation.rus,
                    "eng": item.description_translation.eng,
                    "ukr": item.description_translation.ukr,
                    "pln": item.description_translation.pln,
                    "fra": item.description_translation.fra,
                }
                if item.description_translation is not None
                else None
            ),
        }

    def _random_reward_to_json(self, item: QuestRandomRewardThrough) -> dict:
        return {
            "count": item.count,
            "reward_item": self._random_reward_item_to_json(item.reward),
        }

    def _random_reward_item_to_json(self, reward: QuestRandomReward):
        return {
            "index": reward.index,
            "name": (
                {
                    "rus": reward.name_translation.rus,
                    "eng": reward.name_translation.eng,
                    "ukr": reward.name_translation.ukr,
                    "pln": reward.name_translation.pln,
                    "fra": reward.name_translation.fra,
                }
                if reward.name_translation
                else None
            ),
            "icon_url": (
                reward.icon.icon.url
                if reward.icon is not None and reward.icon.icon is not None
                else None
            ),
        }

    def _camp_to_dict(self, camp: SpawnItem) -> dict:
        position_re = re.compile(r"\s*(?P<x>.*),\s*(?P<y>.*),\s*(?P<z>.*)")
        rm = position_re.match(camp.position_raw)
        if rm is None:
            raise ValueError
        (x, _, z) = float(rm.group("x")), float(rm.group("y")), float(rm.group("z"))
        position = (x, z)
        if camp.location is None:
            raise ValueError("No camp location")
        location_info = LocationMapInfo.objects.get(location=camp.location)
        if location_info.bound_rect_raw:
            offset_re = re.compile(
                r"\s*(?P<min_x>.*),\s*(?P<min_y>.*),\s*(?P<max_x>.*),\s*(?P<max_y>.*)",
            )
            rm = offset_re.match(location_info.bound_rect_raw)
            if rm is None:
                raise ValueError("Не удалось распарсить границы локи")
            (min_x, min_y, max_x, max_y) = (
                float(rm.group("min_x")),
                float(rm.group("min_y")),
                float(rm.group("max_x")),
                float(rm.group("max_y")),
            )
            map_offset = (min_x, min_y, max_x, max_y)
        else:
            map_offset = None
        map_info = None
        location_map_image_url = (
            location_info.map_image.url if location_info.map_image else None
        )
        map_size = (
            (location_info.map_image.width, location_info.map_image.height)
            if location_info.map_image
            else None
        )
        if map_size and location_map_image_url and map_offset:
            map_info = {
                "size": map_size,
                "image_url": location_map_image_url,
                "offset": map_offset,
            }

        translation = camp.location.name_translation
        assert translation is None or isinstance(translation, Translation)
        location_name = (
            {
                "rus": translation.rus,
                "eng": translation.eng,
                "ukr": translation.ukr,
                "pln": translation.pln,
                "fra": translation.fra,
            }
            if translation is not None
            else None
        )
        return {
            "name": camp.name,
            "location_name": location_name,
            "map_info": map_info,
            "position": position,
        }
