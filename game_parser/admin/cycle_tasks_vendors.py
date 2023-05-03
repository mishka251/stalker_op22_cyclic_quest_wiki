from typing import Optional

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import CycleTaskVendor
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


@register(CycleTaskVendor)
class CycleTaskVendorAdmin(ModelAdmin):
    search_fields = (
        'game_story_id_raw',
        'vendor_id',
    )

    list_display = (
        '__str__',
        'game_story_id_raw',
        'vendor_id',
        'game_story_id',
    )

    autocomplete_fields = [
        'game_story_id',
    ]
