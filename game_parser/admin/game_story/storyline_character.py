from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models.game_story import StorylineCharacter, Icon


@register(Icon)
class IconCharacterAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'icon_view',
        'name',
    )

    @display(description='Иконка', )
    def icon_view(self, obj: Icon) -> Optional[str]:
        return mark_safe(f'<img src="{obj.icon.url}" alt="{obj.icon.name}">')


@register(StorylineCharacter)
class StorylineCharacterAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'icon_view',
        'name_view',
    )

    @display(description='Имя')
    def name_view(self, character: StorylineCharacter) -> str:
        return character.get_name

    @display(description='Иконка', )
    def icon_view(self, obj: StorylineCharacter) -> Optional[str]:
        if not obj.icon:
            return None
        return mark_safe(f'<img src="{obj.icon.icon.url}" alt="{obj.icon.icon.name}">')

