from django.urls import reverse
from django.views.generic import TemplateView

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor, QuestKinds


class TaskVendorsList(TemplateView):
    template_name = "wiki/task_vendors_list/task_vendor_list.html"

    def get_context_data(self, **kwargs) -> dict:
        vendors = CycleTaskVendor.objects.all()
        return {
            "vendors": [self._vendor_to_dict(vendor) for vendor in vendors],
        }

    def _vendor_to_dict(self, vendor: CycleTaskVendor) -> dict:
        return {
            "image_path": vendor.icon.icon.url,
            "name": vendor.name_translation.rus,
            "tasks_count": vendor.cyclicquest_set.count(),
            "has_chain": vendor.cyclicquest_set.filter(type=QuestKinds.chain).exists(),
            "quests_link": reverse("vendor_tasks", kwargs={"vendor_id": vendor.id}),
        }
