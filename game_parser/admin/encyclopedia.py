from typing import Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import EncyclopediaGroup, EncyclopediaArticle
from game_parser.utils.admin_utils.icon_view import icon_view


@register(EncyclopediaGroup)
class EncyclopediaGroupAdmin(ModelAdmin):
    autocomplete_fields = [
        "name_translation",
    ]

    search_fields = [
        "name",
        "name_translation__rus",
    ]
    list_display = [
        "name",
        "name_translation",
    ]


@register(EncyclopediaArticle)
class EncyclopediaArticleAdmin(ModelAdmin):
    autocomplete_fields = [
        "name_translation",
        "group",
        "icon",
        "text_translation",
        "artefact",
    ]

    search_fields = [
        "game_id",
        "name",
        "name_translation__rus",
    ]
    list_display = [
        "name_translation",
        "group",
        "text",
        "inv_icon_view",
        "artefact",
    ]

    @display(description="Иконка", )
    def inv_icon_view(self, obj: EncyclopediaArticle) -> Optional[str]:
        if not obj.icon:
            return None
        return icon_view(obj.icon.icon)

