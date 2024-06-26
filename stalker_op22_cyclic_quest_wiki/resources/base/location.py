from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import Location, LocationMapInfo


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        use_natural_foreign_keys = True
        import_id_fields = ["name"]
        exclude = {"id"}


class LocationMapInfoResource(resources.ModelResource):
    class Meta:
        model = LocationMapInfo
        use_natural_foreign_keys = True
        import_id_fields = ["location_name"]
        exclude = {"id"}


__all__ = [
    "LocationMapInfoResource",
    "LocationResource",
]
