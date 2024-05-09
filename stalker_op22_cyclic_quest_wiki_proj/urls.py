from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from stalker_op22_cyclic_quest_wiki.sitemap import sitemaps as wiki_sitemap

sitemaps = {
    **wiki_sitemap,
}

urlpatterns = [
    path(
        "",
        include("stalker_op22_cyclic_quest_wiki.urls"),
        name="stalker_op22_cyclic_quest_wiki",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "game_parser" in settings.INSTALLED_APPS:
    urlpatterns += [
        path("game_parser/", include("game_parser.urls"), name="game_parser"),
    ]
