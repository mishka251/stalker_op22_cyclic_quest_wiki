from typing import TYPE_CHECKING, TypedDict

from django.db.models import Count, Exists, OuterRef, QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor, CyclicQuest
from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import QuestKinds

if TYPE_CHECKING:
    from django_stubs_ext import WithAnnotations


class QuestGiversView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        quests_subquery = CyclicQuest.objects.filter(vendor_id=OuterRef("pk"))
        vendors: (
            "QuerySet[WithAnnotations[CycleTaskVendor, CycleTaskVendorAnnotatedFields]]"
        ) = (
            CycleTaskVendor.objects.all()
            .select_related("icon", "name_translation")
            .annotate(quests_count=Count("quests"))
            .annotate(
                chain_exists=Exists(quests_subquery.filter(type=QuestKinds.CHAIN)),
            )
        )

        results = []
        for quest_giver in vendors:
            quest_giver_json = self._vendor_to_dict(quest_giver)
            results.append(quest_giver_json)
        return JsonResponse(results, safe=False)

    def _vendor_to_dict(
        self,
        vendor: "WithAnnotations[CycleTaskVendor, CycleTaskVendorAnnotatedFields]",
    ) -> dict:
        name_translations = vendor.name_translation
        return {
            "id": str(vendor.id),
            "icon_url": vendor.icon.icon.url,
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
            "tasks_count": vendor.quests_count,
            "has_chain": vendor.chain_exists,
        }


class CycleTaskVendorAnnotatedFields(TypedDict):
    quests_count: int
    chain_exists: bool
