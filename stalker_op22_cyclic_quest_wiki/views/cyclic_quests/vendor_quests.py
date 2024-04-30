from django.http import Http404
from django.views.generic import TemplateView

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor, CyclicQuest
from stalker_op22_cyclic_quest_wiki.views.cyclic_quests.tasks_grouping import (
    collect_vendor_tasks,
)


class VendorQuestsList(TemplateView):
    template_name = "wiki/vendor_quests_list/tasks_list.html"

    def get_context_data(self, vendor_id: int) -> dict:
        try:
            vendor = CycleTaskVendor.objects.get(id=vendor_id)
        except Exception as ex:
            raise Http404("Incorrect vendor ID") from ex
        vendor_tasks = CyclicQuest.objects.filter(vendor=vendor)

        return {
            "vendor_task_info": collect_vendor_tasks(vendor_tasks, vendor),
            "vendor": vendor,
        }
