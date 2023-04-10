from django.contrib.admin import ModelAdmin, register

from game_parser.models import Translation


@register(Translation)
class TranslationAdmin(ModelAdmin):
    search_fields = (
        'code',
        'rus',
    )

    list_display = (
        '__str__',
        'code',
        'rus',
        'eng',
        'ukr',
        'pln',
        'fra',
    )
