from django.contrib.admin import ModelAdmin, display, register
from django.utils.safestring import mark_safe

from game_parser.admin.utils import links_list
from game_parser.models import Dialog, ScriptFunction
from game_parser.models.game_story.dialog import DialogPhrase
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class DialogPhraseInlineAdmin(ReadOnlyNestedTable):
    model = DialogPhrase
    fields = [
        "local_id",
        "text_id_raw",
        "text",
    ]


@register(Dialog)
class DialogAdmin(ModelAdmin):
    inlines = [DialogPhraseInlineAdmin]
    list_display = [
        "__str__",
        "game_id",
    ]

    search_fields = [
        "game_id",
    ]

    autocomplete_fields = [
        "has_info",
        "dont_has_info",
        "give_info",
        "precondition",
        "init_func",
    ]

    readonly_fields = [
        "all_action",
    ]

    @display(description="Функции вызываемые в фразах диалога")
    def all_action(self, dialog: Dialog) -> str:
        all_actions = set(ScriptFunction.objects.filter(starts_phrases__dialog=dialog))
        return mark_safe(links_list(all_actions))


@register(DialogPhrase)
class DialogPhraseAdmin(ModelAdmin):
    list_display = [
        "__str__",
        "dialog",
        "local_id",
        "get_text",
    ]

    autocomplete_fields = [
        "dialog",
        "text",
        "previous",
        "give_info",
        "actions",
        "precondition",
        "has_info",
        "don_has_info",
        "disable_info",
        "disable",
    ]

    search_fields = [
        "local_id",
        "dialog__game_id",
    ]

    @display()
    def get_text(self, phrase: DialogPhrase) -> str | None:
        return phrase.get_text


__all__ = [
    "DialogAdmin",
    "DialogPhraseAdmin",
]
