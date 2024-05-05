from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("stalker_op22_cyclic_quest_wiki.urls"),
        name="stalker_op22_cyclic_quest_wiki",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore[arg-type] # django-example. Working

if "game_parser" in settings.INSTALLED_APPS:
    urlpatterns += [
        path("game_parser/", include("game_parser.urls"), name="game_parser"),
    ]
