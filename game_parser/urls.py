from django.urls import include, path

from game_parser.views import (
    EscapeMap,
    IndexView,
    TasksListView,
    TaskVendorsList,
    VendorQuestsList,
)

app_name = "game_parser"

urlpatterns = [
    path("tasks/", TasksListView.as_view()),
    path("map/", EscapeMap.as_view()),
    path("map/<str:location>", EscapeMap.as_view()),
    path("api/", include("game_parser.api.urls")),
    path("task_vendors/", TaskVendorsList.as_view(), name="task_vendors"),
    path(
        "task_vendors/<int:vendor_id>/quests/",
        VendorQuestsList.as_view(),
        name="vendor_tasks",
    ),
    path("", IndexView.as_view(), name="index"),
]
