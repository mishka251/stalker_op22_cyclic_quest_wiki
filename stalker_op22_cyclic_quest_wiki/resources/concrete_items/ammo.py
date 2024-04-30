from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import Ammo


class AmmoResource(resources.ModelResource):

    class Meta:
        model = Ammo
        use_natural_foreign_keys = True
        import_id_fields=["name"]

        exclude = {"id", "item_ptr", "polymorphic_ctype"}
