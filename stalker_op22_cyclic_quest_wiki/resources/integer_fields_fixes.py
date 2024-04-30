from import_export import widgets
from import_export.resources import ModelResource

ModelResource.WIDGETS_MAP["PositiveBigIntegerField"] = widgets.IntegerWidget
ModelResource.WIDGETS_MAP["PositiveSmallIntegerField"] = widgets.IntegerWidget