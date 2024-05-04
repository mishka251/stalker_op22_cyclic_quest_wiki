from collections.abc import Iterable, Sequence
from typing import Any, Optional

from django.apps import AppConfig, apps
from django.apps.registry import Apps
from django.contrib.admin import site as admin_site
from django.core import checks
from django.db import models


@checks.register()
def check_model_admin_fields(
        *,
        app_configs: Sequence[AppConfig] | None,
        databases: Sequence[str] | None,
        **kwargs: Any
) -> Iterable[checks.CheckMessage]:
    errors: list[checks.CheckMessage] = []
    apps_: Iterable[AppConfig] = app_configs or apps.get_app_configs()
    for app_config in apps_:
        for model in app_config.get_models():
            model_admin = admin_site._registry.get(model)
            if not model_admin:
                continue
            model_fk_field_names = {
                field.name
                for field in model._meta.get_fields()
                if isinstance(field, models.ForeignKey)
                and field.editable
                and not field.auto_created
            }
            autocomplete_fields = set(model_admin.autocomplete_fields or [])
            not_autocomplete_fields = model_fk_field_names - autocomplete_fields
            for field_name in not_autocomplete_fields:
                warning = checks.Warning(
                    f"ForeignKey {field_name} не найден в autocomplete_fields",
                    obj=model_admin,
                )
                errors.append(warning)
    return errors
