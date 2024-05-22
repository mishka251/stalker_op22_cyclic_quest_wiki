from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, JsonResponse
from django.views.generic import View

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor, CyclicQuest
from stalker_op22_cyclic_quest_wiki.views.cyclic_quests.tasks_grouping import (
    Quest,
    QuestTarget,
    TaskReward,
    collect_vendor_tasks,
)


class VendorCyclicQuests(View):
    def get(self, request: HttpRequest, vendor_id: int) -> HttpResponse:
        vendor = self._get_vendor(vendor_id)
        vendor_tasks = list(
            CyclicQuest.objects.filter(vendor_id=vendor_id)
            .select_related("text")
            .prefetch_related("itemreward_set__item__name_translation")
            .prefetch_related("itemreward_set__item__icon")
            .prefetch_related("moneyreward_set")
            .prefetch_related("questrandomreward_set__reward__icon")
            .prefetch_related("questrandomreward_set__reward__description")
            .prefetch_related("treasurereward_set"),
        )

        vendor_task_info = collect_vendor_tasks(vendor_tasks, vendor)
        results = []
        for quest_kind, quests_by_prior in vendor_task_info.quest_group_by_type.items():
            quest_kind_json = {
                "value": str(quest_kind.value),
                "label": str(quest_kind.label),
            }
            for prior, quests in quests_by_prior.items():
                for quest in quests:
                    quest_json = self._quest_to_dict(prior, quest, quest_kind_json)
                    results.append(quest_json)
        return JsonResponse(results, safe=False)

    def _quest_to_dict(self, prior: int, quest: Quest, quest_kind_json: dict) -> dict:
        return {
            "kind": quest_kind_json,
            "prior": prior,
            "text": quest.text,
            "target": self._target_to_json(quest.target),
            "rewards": [self._reward_to_json(reward) for reward in quest.rewards],
        }

    def _get_vendor(self, vendor_id: int) -> CycleTaskVendor:
        try:
            vendor = CycleTaskVendor.objects.select_related("name_translation").get(
                id=vendor_id,
            )
        except Exception as ex:
            msg = "Incorrect vendor ID"
            raise Http404(msg) from ex
        return vendor

    def _target_to_json(self, target: QuestTarget) -> dict:
        return target.to_json()

    def _reward_to_json(self, reward: TaskReward) -> dict:
        return reward.to_json()
