from django.urls import path

from stalker_op22_cyclic_quest_wiki.views.api.cz import VendorCyclicQuests
from stalker_op22_cyclic_quest_wiki.views.api.items.search import ItemsSearchAPI
from stalker_op22_cyclic_quest_wiki.views.api.items.where_find import WhereFindItemAPI
from stalker_op22_cyclic_quest_wiki.views.api.items.where_need import WhereNeedItemAPI
from stalker_op22_cyclic_quest_wiki.views.api.vendors import QuestGiversView

app_name = "api"

urlpatterns = [
    path("quest_vendors/", QuestGiversView.as_view(), name="task_vendors"),
    path("items/", ItemsSearchAPI.as_view(), name="items"),
    path(
        "items/<int:item_id>/where_find",
        WhereFindItemAPI.as_view(),
        name="where_find_item",
    ),
    path(
        "items/<int:item_id>/where_need",
        WhereNeedItemAPI.as_view(),
        name="where_need_item",
    ),
    path(
        "quest_vendors/<int:vendor_id>/quests/",
        VendorCyclicQuests.as_view(),
        name="vendor_tasks",
    ),
]
