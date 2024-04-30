from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import Translation


class TranslationResource(resources.ModelResource):

    class Meta:
        model = Translation
        use_natural_foreign_keys = True
        import_id_fields=["code"]
        exclude = {"id"}

__all__ = [
    "TranslationResource",
]

