from import_export import fields, resources
from import_export.widgets import ManyToManyWidget

from stalker_op22_cyclic_quest_wiki.models import Item, ItemReward, MoneyReward, QuestRandomReward, RandomRewardInfo, TreasureReward


class ItemRewardResource(resources.ModelResource):
    class Meta:
        model = ItemReward
        use_natural_foreign_keys = True
        import_id_fields = ["quest", "item"]
        exclude = {"id", "polymorphic_ctype"}



class MoneyRewardResource(resources.ModelResource):
    class Meta:
        model = MoneyReward
        use_natural_foreign_keys = True
        import_id_fields = ["quest"]
        exclude = {"id", "polymorphic_ctype"}



class QuestRandomRewardResource(resources.ModelResource):
    class Meta:
        model = QuestRandomReward
        use_natural_foreign_keys = True
        import_id_fields = ["quest", "reward"]
        exclude = {"id", "polymorphic_ctype"}
class RandomRewardInfoResource(resources.ModelResource):
    class Meta:
        model = RandomRewardInfo
        use_natural_foreign_keys = True
        import_id_fields = ["index"]
        exclude = {"id"}

    possible_items = fields.Field(
        column_name="possible_items",
        attribute="possible_items",
        widget=ManyToManyWidget(Item, separator="|", field="name"),
    )



class TreasureRewardResource(resources.ModelResource):
    class Meta:
        model = TreasureReward
        use_natural_foreign_keys = True
        import_id_fields = ["quest"]
        exclude = {"id", "polymorphic_ctype"}
