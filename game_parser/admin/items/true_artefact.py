from django.contrib.admin import ModelAdmin, register

from game_parser.models import TrueArtefact


@register(TrueArtefact)
class TrueArtefactAdmin(ModelAdmin):
    pass
