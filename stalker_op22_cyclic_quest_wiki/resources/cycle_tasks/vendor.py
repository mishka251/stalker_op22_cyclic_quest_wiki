from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor


class CycleTaskVendorResource(resources.ModelResource):

    class Meta:
        model = CycleTaskVendor
        use_natural_foreign_keys = True
        import_id_fields=["section_name"]
        exclude = {"id"}

__all__ = [
    "CycleTaskVendorResource",
]
