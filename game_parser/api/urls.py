from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from game_parser.api.cz import QuestGiversView, VendorCyclicQuests
from game_parser.views import TasksListView, EscapeMap

urlpatterns = [
    path('quest_vendors/', QuestGiversView.as_view()),
    path('quests/', VendorCyclicQuests.as_view()),
]
