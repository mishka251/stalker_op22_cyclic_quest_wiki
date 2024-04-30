from django.db.models import Model
from import_export.widgets import ManyToManyWidget


class ManyToManyNaturalKeyField(ManyToManyWidget):
    def __init__(self, model, **kwargs):
        kwargs.setdefault("field", "pk")
        super().__init__(model, **kwargs)

    def clean(self, value, row=None, **kwargs) -> list[Model]:
        if not value:
            return self.model.objects.none()
        if isinstance(value, (tuple)):
            ids = [value]
        else:
            ids = value.split(self.separator)
            ids = filter(None, [i.strip() for i in ids])
        items = [
            self.model.objects.get_by_natural_key(key)
            for key in ids
        ]
        return items

    def render(self, value, obj=None) -> str:
        ids = [str(obj.natural_key()) for obj in value.all()]
        return self.separator.join(ids)
