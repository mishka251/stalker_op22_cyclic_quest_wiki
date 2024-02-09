import re
from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.template import loader

from game_parser.models import SpawnItem, NpcLogicConfig, CustomSpawnItem, LocationMapInfo, Recept
from game_parser.utils.admin_utils.icon_view import icon_view

@register(Recept)
class ReceptAdmin(ModelAdmin):
    autocomplete_fields = [
        "condition",
        "components",
        "cel",
        "info",
    ]

    list_display = [
        "__str__",
        "anomaly_id",
        "anomaly_name",
        "condition",
        # "components",
        "cel",
    ]