from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import MapPosition


class MapPositionResource(resources.ModelResource):
    class Meta:
        model = MapPosition
        use_natural_foreign_keys = True
        import_id_fields = ["spawn_id"]
        exclude = {"id"}
        use_bulk = True


__all__ = [
    "MapPositionResource",
]
