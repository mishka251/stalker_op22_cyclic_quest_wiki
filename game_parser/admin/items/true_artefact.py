from django.contrib.admin import register

from game_parser.admin.items.base_item_admin import BaseItemAdmin
from game_parser.models import TrueArtefact


@register(TrueArtefact)
class TrueArtefactAdmin(BaseItemAdmin):
    list_display: tuple[str, ...] = (
        *BaseItemAdmin.list_display,
        "health_restore_speed",
        "burn_immunity",
        "strike_immunity",
        "shock_immunity",
        "wound_immunity",
        "radiation_immunity",
        "telepatic_immunity",
        "chemical_burn_immunity",
        "explosion_immunity",
        "fire_wound_immunity",
        "power_restore_speed",
        "additional_weight",
        "radiation_restore_speed",
        "bleeding_restore_speed",
    )
