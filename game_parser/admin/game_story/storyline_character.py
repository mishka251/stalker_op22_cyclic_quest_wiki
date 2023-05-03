from typing import Optional

from django.contrib.admin import ModelAdmin, register, display
from django.utils.html import mark_safe

from game_parser.models import Dialog, GameStoryId
from game_parser.models.game_story import StorylineCharacter, Icon
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


@register(Icon)
class IconCharacterAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'icon_view',
        'name',
    )
    search_fields = ['name']

    @display(description='Иконка', )
    def icon_view(self, obj: Icon) -> Optional[str]:
        return mark_safe(f'<img src="{obj.icon.url}" alt="{obj.icon.name}">')


class DialogInlineAdmin(ReadOnlyNestedTable):
    model = StorylineCharacter.dialogs.through


class GameStoryIdAdmin(ReadOnlyNestedTable):
    model = GameStoryId


@register(StorylineCharacter)
class StorylineCharacterAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'icon_view',
        'name_view',
    )
    search_fields = ['name', 'name_translation__rus']
    autocomplete_fields = [
        'name_translation',
        'icon',
        'dialogs',
    ]

    inlines = [
        DialogInlineAdmin,
        GameStoryIdAdmin,
    ]

    @display(description='Имя')
    def name_view(self, character: StorylineCharacter) -> str:
        return character.get_name

    @display(description='Иконка', )
    def icon_view(self, obj: StorylineCharacter) -> Optional[str]:
        if not obj.icon:
            return None
        return mark_safe(f'<img src="{obj.icon.icon.url}" alt="{obj.icon.icon.name}">')

