import dataclasses
from pathlib import Path

import tablib
from django.core.management import BaseCommand, CommandError
from django.db.models import Model
from import_export.results import Error

from stalker_op22_cyclic_quest_wiki.management.commands.resources import to_export


class Command(BaseCommand):
    def handle(self, *args, **options):
        tmp_dir = Path("export_tmp")
        for model_info in to_export:
            print(f"start {model_info.model_cls.__name__}")
            file_path = tmp_dir/model_info.file_name
            resource = model_info.resource_cls()
            with open(file_path, "r", encoding="utf-8") as file:
                dataset = tablib.Dataset().load(file.read(), format="csv")
            result = resource.import_data(dataset)
            if result.has_errors():
                print("ERROR")
                if result.base_errors:
                    print("base_errors")
                    for error in result.base_errors:
                        self._print_error(error)
                if result.row_errors():
                    print("row_errors")
                    for (row_num, row_errors) in result.row_errors():
                        print(row_num)
                        for error in row_errors:
                            self._print_error(error)
                raise CommandError("Импорт сломался")
            else:
                print(f"end {model_info.model_cls.__name__} OK")

    def _print_error(self, error: Error):
        print(f"{error.error} {error.row}\n{error.traceback}")