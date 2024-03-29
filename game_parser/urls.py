from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from game_parser.views import TasksListView, EscapeMap, TaskVendorsList

urlpatterns = [
    path('tasks/', TasksListView.as_view()),
    path('map/', EscapeMap.as_view()),
    path('map/<str:location>', EscapeMap.as_view()),
    path("api/", include("game_parser.api.urls")),
    path("task_vendors/", TaskVendorsList.as_view())
]
