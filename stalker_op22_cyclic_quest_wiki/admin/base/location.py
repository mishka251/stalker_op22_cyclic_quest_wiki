from django.contrib.admin import ModelAdmin, register

from stalker_op22_cyclic_quest_wiki.models import Location, LocationMapInfo


@register(Location)
class LocationAdmin(ModelAdmin):
    pass

@register(LocationMapInfo)
class LocationMapInfoAdmin(ModelAdmin):
    pass

