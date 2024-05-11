from django.urls import path

from stalker_op22_cyclic_quest_wiki.views.cyclic_quests.vendor_quests import (
    VendorQuestsList,
)
from stalker_op22_cyclic_quest_wiki.views.cyclic_quests.vendors_list import (
    TaskVendorsList,
)
from stalker_op22_cyclic_quest_wiki.views.index import IndexView
from stalker_op22_cyclic_quest_wiki.views.items.list import ItemsListView

urlpatterns = [
    path("task_vendors/", TaskVendorsList.as_view(), name="task_vendors"),
    path(
        "task_vendors/<int:vendor_id>/quests/",
        VendorQuestsList.as_view(),
        name="vendor_tasks",
    ),
    path("items/", ItemsListView.as_view(), name="items"),
    path("", IndexView.as_view(), name="index"),
]
