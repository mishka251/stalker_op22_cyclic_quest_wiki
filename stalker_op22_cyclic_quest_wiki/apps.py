from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class StalkerOp22CyclicQuestWikiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stalker_op22_cyclic_quest_wiki"

    def ready(self) -> None:
        super().ready()
        autodiscover_modules("checks")
