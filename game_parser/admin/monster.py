from django.contrib.admin import ModelAdmin, display, register

from game_parser.models import Monster
from game_parser.utils.admin_utils.icon_view import icon_view


@register(Monster)
class MonsterAdmin(ModelAdmin):
    autocomplete_fields = [
        "monster_part",
        "icon",
        "name_translation",
    ]

    search_fields = [
        "section_name",
        "short_name",
    ]
    list_display = [
        "name_translation",
        "section_name",
        "short_name",
        "terrain",
        "spec_rank",
        "class_name",
        "monster_part",
        "inv_icon_view",
    ]

    @display(description="Иконка")
    def inv_icon_view(self, obj: Monster) -> str | None:
        if not obj.icon:
            return None
        return icon_view(obj.icon.icon)
