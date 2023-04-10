from django.contrib.admin import ModelAdmin, register, TabularInline, display

from game_parser.models import Dialog
from game_parser.models.game_story.dialog import DialogPhrase


class DialogPhraseInlineAdmin(TabularInline):
    model = DialogPhrase
    show_change_link = True
    list_display = [
        # '__str__',
        'local_id',
        # 'text_id_raw',
        # 'text',
        'get_text',
    ]

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @display()
    def get_text(self, phrase: DialogPhrase):
        return phrase.get_text


@register(Dialog)
class DialogAdmin(ModelAdmin):
    inlines = [DialogPhraseInlineAdmin]
    list_display = [
        '__str__',
        'game_id',
    ]

    filter_horizontal = [
        'has_info',
        'dont_has_info',
        'give_info',
        'precondition',
        'init_func',
    ]

    search_fields = [
        'game_id',
    ]


@register(DialogPhrase)
class DialogPhraseAdmin(ModelAdmin):
    list_display = [
        '__str__',
        'dialog',
        'local_id',
        'get_text',
    ]

    autocomplete_fields = [
        'dialog',
        'text',
        'previous',
        'give_info',
        'actions',
        'precondition',
        'has_info',
        'don_has_info',
        'disable_info',
        'disable',
    ]

    search_fields = [
        'local_id',
        'dialog',
    ]

    @display()
    def get_text(self, phrase: DialogPhrase):
        return phrase.get_text
