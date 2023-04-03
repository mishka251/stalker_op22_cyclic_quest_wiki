from django.contrib.admin import ModelAdmin, register, TabularInline

from game_parser.models import Dialog
from game_parser.models.game_story.dialog import DialogPhrase


class DialogPhraseInlineAdmin(TabularInline):
    model = DialogPhrase

@register(Dialog)
class DialogAdmin(ModelAdmin):
    inlines = [DialogPhraseInlineAdmin]

@register(DialogPhrase)
class DialogPhraseAdmin(ModelAdmin):
    pass