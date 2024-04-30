from import_export import resources

from stalker_op22_cyclic_quest_wiki.models import CyclicQuest


class CyclicQuestResource(resources.ModelResource):

    class Meta:
        model = CyclicQuest
        use_natural_foreign_keys = True
        import_id_fields=["game_code"]
        exclude = {"id"}