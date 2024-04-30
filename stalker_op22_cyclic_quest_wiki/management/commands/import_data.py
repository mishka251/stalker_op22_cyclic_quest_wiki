import shutil
import zipfile
from pathlib import Path

import tablib
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from import_export.results import Error

from stalker_op22_cyclic_quest_wiki.management.commands.resources import to_export


class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--imported_archive",
            type=Path,
            help="Path to imported file",
            default=Path("data.zip"),
        )

    def handle(self, *args, **options):
        imported_archive = options["imported_archive"]
        tmp_dir = Path("import_tmp")
        tmp_dir.mkdir(exist_ok=True)

        with zipfile.ZipFile(imported_archive, "r") as myzip:
            myzip.extractall(tmp_dir)
        for model_info in to_export:
            print(f"start {model_info.model_cls.__name__}")
            file_path = tmp_dir / model_info.file_name
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

        print("Start import icons")
        icons_dir = tmp_dir / "icons"
        media_dir = Path(settings.MEDIA_ROOT)
        media_dir.mkdir(exist_ok=True)
        for icon_path in icons_dir.iterdir():
            if icon_path.is_dir():
                shutil.copytree(icon_path, media_dir / icon_path.name, dirs_exist_ok=True)
            else:
                shutil.copyfile(icon_path, media_dir / icon_path.name)
        print("End import icons")

        print("Start import maps")
        maps_dir = tmp_dir / "maps"
        for map_path in maps_dir.iterdir():
            if map_path.is_dir():
                shutil.copytree(map_path, media_dir / map_path.name, dirs_exist_ok=True)
            else:
                shutil.copyfile(map_path, media_dir / map_path.name)
        print("End import maps")
        shutil.rmtree(tmp_dir)

    def _print_error(self, error: Error):
        print(f"{error.error} {error.row}\n{error.traceback}")
