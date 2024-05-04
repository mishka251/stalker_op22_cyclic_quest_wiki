from django.db.models import Model
from import_export.widgets import ManyToManyWidget


class ManyToManyNaturalKeyField(ManyToManyWidget):
    def __init__(self, model, **kwargs):
        kwargs.setdefault("field", "pk")
        super().__init__(model, **kwargs)

    def clean(self, value, row=None, **kwargs) -> list[Model]:
        if not value:
            return self.model.objects.none()
        ids: list[tuple[str, ...]] = (
            [value]
            if isinstance(value, tuple)
            else [
                i.strip().split(",")
                for i in value.split(self.separator)
                if i is not None
            ]
        )
        return [self.model.objects.get_by_natural_key(*key) for key in ids]

    def render(self, value, obj=None) -> str:
        ids = [str(obj.natural_key()) for obj in value.all()]
        return self.separator.join(ids)
