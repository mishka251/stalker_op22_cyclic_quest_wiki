from django.urls import path

from game_parser.api.cz import QuestGiversView, VendorCyclicQuests

urlpatterns = [
    path("quest_vendors/", QuestGiversView.as_view()),
    path("quests/", VendorCyclicQuests.as_view()),
]
