import dataclasses
from pathlib import Path

from django.core.management import BaseCommand
from django.db.models import Model

from stalker_op22_cyclic_quest_wiki.management.commands.resources import to_export


class Command(BaseCommand):
    def handle(self, *args, **options):
        tmp_dir = Path("export_tmp")
        tmp_dir.mkdir(exist_ok=True, parents=True)
        for model_info in to_export:
            resource = model_info.resource_cls()
            dataset = resource.export()
            with open(tmp_dir/model_info.file_name, "w", encoding="utf-8") as file:
                file.write(dataset.csv)