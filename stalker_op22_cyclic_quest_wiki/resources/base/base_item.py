from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import Ammo, Item


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        use_natural_foreign_keys = True
        import_id_fields = ["name"]
        exclude = {"id", "polymorphic_ctype"}
        use_bulk = True

    def get_queryset(self) -> QuerySet[Item]:
        qs = super().get_queryset()
        ammo = ContentType.objects.get_for_model(Ammo)
        return qs.exclude(polymorphic_ctype=ammo)


__all__ = [
    "ItemResource",
]
