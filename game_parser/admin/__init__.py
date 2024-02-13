from django.apps import apps
from django.apps.registry import Apps
from django.contrib.admin.sites import site as admin_site
from django.core import checks
from django.db import models

from .anomaly import *
from .custom_inventory_box import *
from .cycle_tasks_vendors import *
from .encyclopedia import *
from .game_story import *
from .game_story_ids import *
from .items import *
from .locations import *
from .monster import *
from .quest import QuestAdmin
from .quest_random_reward import *
from .recept import *
from .spawn_item import *
from .trade import *
from .translation import *
from .treasures import *


@checks.register()
def check_model_admin_fields(app_configs: Optional[Apps], **kwargs):
    errors = []
    apps_: Apps = app_configs or apps
    for app_config in apps_.get_app_configs():
        for model in app_config.get_models():
            model_admin = admin_site._registry.get(model)
            if not model_admin:
                continue
            model_fk_field_names = {
                field.name
                for field in model._meta.get_fields()
                if isinstance(field, models.ForeignKey) and field.editable and not field.auto_created
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
