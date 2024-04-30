from import_export import resources, fields
from import_export.widgets import ManyToManyWidget

from stalker_op22_cyclic_quest_wiki.models import CycleTaskTargetCamp, MapPosition, Community
from stalker_op22_cyclic_quest_wiki.models import CycleTaskTargetItem
from stalker_op22_cyclic_quest_wiki.models import CycleTaskTargetStalker


class CycleTaskTargetCampResource(resources.ModelResource):
    class Meta:
        model = CycleTaskTargetCamp
        use_natural_foreign_keys = True
        import_id_fields = ["quest"]
        exclude = {"id", "polymorphic_ctype", "cycletasktarget_ptr"}

    communities = fields.Field(
        column_name="communities",
        attribute="communities",
        widget=ManyToManyWidget(Community, separator="|", field="name")
    )


class CycleTaskTargetItemResource(resources.ModelResource):
    class Meta:
        model = CycleTaskTargetItem
        use_natural_foreign_keys = True
        import_id_fields = ["quest"]
        exclude = {"id", "polymorphic_ctype", "cycletasktarget_ptr"}

class CycleTaskTargetStalkerResource(resources.ModelResource):
    class Meta:
        model = CycleTaskTargetStalker
        use_natural_foreign_keys = True
        import_id_fields = ["quest"]
        exclude = {"id", "polymorphic_ctype", "cycletasktarget_ptr"}

    map_positions = fields.Field(
        column_name="map_positions",
        attribute="map_positions",
        widget=ManyToManyWidget(MapPosition, separator="|", field="spawn_id")
    )

