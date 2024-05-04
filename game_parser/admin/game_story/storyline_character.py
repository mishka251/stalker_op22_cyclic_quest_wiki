from django.contrib.admin import ModelAdmin, display, register
from django.utils.safestring import mark_safe

from game_parser.models import Community, GameStoryId, Rank
from game_parser.models.game_story import Icon, StorylineCharacter
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


@register(Icon)
class IconCharacterAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "icon_view",
        "name",
    )
    search_fields = ["name"]

    @display(description="Иконка")
    def icon_view(self, obj: Icon) -> str | None:
        return mark_safe(f'<img src="{obj.icon.url}" alt="{obj.icon.name}">')


class DialogInlineAdmin(ReadOnlyNestedTable):
    model = StorylineCharacter.dialogs.through


class GameStoryIdAdmin(ReadOnlyNestedTable):
    model = GameStoryId


@register(Community)
class CommunityAdmin(ModelAdmin):
    search_fields = [
        "index",
        "code",
    ]

    autocomplete_fields = [
        "translation",
    ]


@register(Rank)
class RandAdmin(ModelAdmin):
    search_fields = [
        "name",
    ]

    autocomplete_fields = [
        "translation",
    ]


@register(StorylineCharacter)
class StorylineCharacterAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "icon_view",
        "name_view",
    )
    search_fields = ["name", "name_translation__rus"]
    autocomplete_fields = [
        "name_translation",
        "icon",
        "dialogs",
        "community",
    ]

    inlines = [
        DialogInlineAdmin,
        GameStoryIdAdmin,
    ]

    @display(description="Имя")
    def name_view(self, character: StorylineCharacter) -> str:
        return character.get_name

    @display(description="Иконка")
    def icon_view(self, obj: StorylineCharacter) -> str | None:
        if not obj.icon:
            return None
        return mark_safe(f'<img src="{obj.icon.icon.url}" alt="{obj.icon.icon.name}">')


__all__ = [
    "IconCharacterAdmin",
    "CommunityAdmin",
    "RandAdmin",
    "StorylineCharacterAdmin",
]
