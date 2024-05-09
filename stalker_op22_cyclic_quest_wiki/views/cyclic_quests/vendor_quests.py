from django.http import Http404
from django.views.generic import TemplateView

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor, CyclicQuest
from stalker_op22_cyclic_quest_wiki.views.cyclic_quests.tasks_grouping import (
    collect_vendor_tasks,
)


class VendorQuestsList(TemplateView):
    template_name = "wiki/vendor_quests_list/tasks_list.html"

    #  pylint: disable=arguments-differ
    def get_context_data(self, vendor_id: int) -> dict:  # type: ignore[override] # зависит от конфига url-ов. Думаю так лучше
        try:
            vendor = CycleTaskVendor.objects.select_related("name_translation").get(
                id=vendor_id,
            )
        except Exception as ex:
            raise Http404("Incorrect vendor ID") from ex
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

        return {
            "vendor_task_info": vendor_task_info,
            "vendor": vendor,
            "meta_description": f"Сталкер ОП-2.2 Циклические квесты от {vendor}",
            "meta_keywords": f"сталкер, stalker, объединенный пак 2.2, циклические квесты, ОП-2.2, {vendor}",
        }
