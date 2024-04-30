from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import Community
from stalker_op22_cyclic_quest_wiki.models import StalkerRank


class CommunityResource(resources.ModelResource):

    class Meta:
        model = Community
        use_natural_foreign_keys = True
        import_id_fields=["name"]
        exclude = {"id"}


class StalkerRankResource(resources.ModelResource):

    class Meta:
        model = StalkerRank
        use_natural_foreign_keys = True
        import_id_fields=["name"]
        exclude = {"id"}
