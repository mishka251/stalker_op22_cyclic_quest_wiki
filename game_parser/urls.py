from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from game_parser.views import TasksListView

urlpatterns = [
    path('tasks/', TasksListView.as_view()),
]
