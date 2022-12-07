from django.contrib.admin import ModelAdmin, register

from game_parser.models import Scope


@register(Scope)
class ScopeAdmin(ModelAdmin):
    pass
