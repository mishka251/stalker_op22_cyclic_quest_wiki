from decimal import Decimal
from typing import Any, Optional, Type
from django.db.models import Model

SECTION_NAME = '_section_name'


class BaseResourceField:
    _required: bool = True
    _data_field_name: str
    _model_field_name: str
    _default: Any = None

    def __init__(
            self,
            data_field_name: str,
            model_field_name: Optional[str] = None,
            required: bool = True,
            default=None,
    ):
        self._data_field_name = data_field_name
        if model_field_name:
            self._model_field_name = model_field_name
        else:
            self._model_field_name = data_field_name
        self._required = required
        self._default = default

    def _get_from_data(self, data: dict[str, Any]) -> Any:
        if self._required:
            return data.pop(self._data_field_name)
        else:
            return data.pop(self._data_field_name, self._default)

    def _parse_value(self, value: Any) -> Any:
        if value is None:
            return None
        return self._parse_non_empty_value(value)

    def _parse_non_empty_value(self, value: Any):
        raise NotImplementedError()

    def get_value(self, data: dict[str, Any]) -> Any:
        value = self._get_from_data(data)
        return self._parse_value(value)

    def fill_instance(self, instance, value):
        setattr(instance, self._model_field_name, value)


class CharField(BaseResourceField):
    def _parse_non_empty_value(self, value: Any) -> Any:
        return str(value)


class DecimalField(BaseResourceField):
    def _parse_non_empty_value(self, value: Any) -> Any:
        return Decimal(value)


class IntegerField(BaseResourceField):
    def _parse_non_empty_value(self, value: Any) -> Any:
        return int(value)


class BooleanField(BaseResourceField):
    def __init__(
            self,
            data_field_name: str,
            model_field_name: Optional[str] = None,
            required: bool = False,
            default=False,
    ):
        super().__init__(data_field_name, model_field_name, required, default)

    def _parse_non_empty_value(self, value: Any) -> Any:
        TRUE_VALUE = 'true'
        return value == TRUE_VALUE


class BaseModelResource:
    _fields: list[BaseResourceField]
    _model_cls: Type[Model]
    _exclude_fields: set[str] = set()

    def get_fields(self):
        return self._fields

    def _init_instance(self):
        return self._model_cls()

    def _apply_data(self, data: dict[str, Any], instance):
        for field in self.get_fields():
            value = field.get_value(data)
            field.fill_instance(instance, value)

    def create_instance_from_data(self, section_name: str, data: dict[str, Any]):
        data[SECTION_NAME] = section_name,
        instance = self._init_instance()
        self._apply_data(data, instance)
        self._save_instance(instance)
        for field_name in list(data.keys()):
            if field_name in self._exclude_fields:
                data.pop(field_name)
        return instance

    def _save_instance(self, instance):
        instance.save()
