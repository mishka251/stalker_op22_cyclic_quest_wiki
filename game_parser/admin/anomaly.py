from django.contrib.admin import ModelAdmin, register

from game_parser.models import Anomaly


@register(Anomaly)
class AnomalyAdmin(ModelAdmin):
    autocomplete_fields = [
        "article",
    ]

    search_fields = [
        "section_name",
        "class_name",
    ]
    list_display = [
        "section_name",
        "class_name",
        "article",
    ]
