from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.safestring import mark_safe

from game_parser.models.items.base_item import BaseItem


@register(BaseItem)
class BaseItemAdmin(ModelAdmin):
    list_display = (
        'name_translation_rus',
        'description_translation_rus',
        'inv_icon_view',
    )

    search_fields = [
        'inv_name',
        'name',
    ]


    @display(description='Название', ordering='name_translation__rus')
    def name_translation_rus(self, obj: BaseItem) -> str:
        if obj.name_translation:
            return obj.name_translation.rus
        return obj.inv_name

    @display(description='Описание')
    def description_translation_rus(self, obj: BaseItem) -> str:
        if obj.description_translation:
            return obj.description_translation.rus
        return obj.description_code

    @display(description='Иконка', )
    def inv_icon_view(self, obj: BaseItem) -> Optional[str]:
        if not obj.inv_icon:
            return None
        return mark_safe(f'<img src="{obj.inv_icon.url}" alt="{obj.inv_icon.name}">')
