from django.urls import path

from stalker_op22_cyclic_quest_wiki.views.api.cz import VendorCyclicQuests
from stalker_op22_cyclic_quest_wiki.views.api.vendors import QuestGiversView

app_name = "api"

urlpatterns = [
    path("quest_vendors/", QuestGiversView.as_view(), name="task_vendors"),
    path(
        "quest_vendors/<int:vendor_id>/quests/",
        VendorCyclicQuests.as_view(),
        name="vendor_tasks",
    ),
]
