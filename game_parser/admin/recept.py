from django.contrib.admin import ModelAdmin, register

from game_parser.models import Recept


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
