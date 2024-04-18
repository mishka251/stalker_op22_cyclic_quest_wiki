from import_export.resources import ModelResource
from import_export import widgets

ModelResource.WIDGETS_MAP["PositiveBigIntegerField"] = widgets.IntegerWidget
ModelResource.WIDGETS_MAP["PositiveSmallIntegerField"] = widgets.IntegerWidget