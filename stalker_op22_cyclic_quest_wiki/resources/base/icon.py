from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import Icon


class IconResource(resources.ModelResource):

    class Meta:
        model = Icon
        use_natural_foreign_keys = True
        import_id_fields=["name"]
        exclude = {"id"}