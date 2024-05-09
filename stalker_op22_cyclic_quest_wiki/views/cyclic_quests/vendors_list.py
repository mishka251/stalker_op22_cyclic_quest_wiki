from typing import TYPE_CHECKING, TypedDict

from django.db.models import Count, Exists, OuterRef, QuerySet
from django.urls import reverse
from django.views.generic import TemplateView

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor, CyclicQuest
from stalker_op22_cyclic_quest_wiki.models.cycle_tasks.cycle_task import QuestKinds

if TYPE_CHECKING:
    from django_stubs_ext import WithAnnotations


class CycleTaskVendorAnnotatedFields(TypedDict):
    quests_count: int
    chain_exists: bool


class TaskVendorsList(TemplateView):
    template_name = "wiki/task_vendors_list/task_vendor_list.html"

    def get_context_data(self, **kwargs) -> dict:
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
        return {
            "vendors": [self._vendor_to_dict(vendor) for vendor in vendors],
        }

    def _vendor_to_dict(
        self,
        vendor: "WithAnnotations[CycleTaskVendor, CycleTaskVendorAnnotatedFields]",
    ) -> dict:
        return {
            "image_path": vendor.icon.icon.url,
            "name": vendor.name_translation.rus,
            "tasks_count": vendor.quests_count,
            "has_chain": vendor.chain_exists,
            "quests_link": reverse("vendor_tasks", kwargs={"vendor_id": vendor.id}),
        }
