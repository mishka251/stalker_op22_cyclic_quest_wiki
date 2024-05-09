from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet
from django.urls import reverse

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor


class VendorsListSitemap(Sitemap):
    def items(self) -> list[str]:
        return ["task_vendors"]

    def location(self, item: str) -> str:
        return reverse(item)


class VendorsQuestsSitemap(Sitemap):
    def location(self, item: CycleTaskVendor) -> str:
        return reverse("vendor_tasks", kwargs={"vendor_id": item.id})

    def items(self) -> QuerySet[CycleTaskVendor]:
        return CycleTaskVendor.objects.all()


sitemaps = {
    "vendors_list": VendorsListSitemap,
    "vendors_quests": VendorsQuestsSitemap,
}
