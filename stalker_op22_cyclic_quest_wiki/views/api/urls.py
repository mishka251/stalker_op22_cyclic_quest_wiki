from django.urls import path

from stalker_op22_cyclic_quest_wiki.views.api.cz import VendorCyclicQuests
from stalker_op22_cyclic_quest_wiki.views.api.vendors import QuestGiversView

urlpatterns = [
    path("quest_vendors/", QuestGiversView.as_view()),
    path("quest_vendors/<int:vendor_id>/quests/", VendorCyclicQuests.as_view()),
]
