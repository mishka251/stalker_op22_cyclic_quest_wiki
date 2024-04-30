import shutil
from pathlib import Path

from django.core.management import BaseCommand

from stalker_op22_cyclic_quest_wiki.management.commands.resources import to_export
from stalker_op22_cyclic_quest_wiki.models import Icon, LocationMapInfo


class Command(BaseCommand):
    def handle(self, *args, **options):
        tmp_dir = Path("export_tmp")
        tmp_dir.mkdir(exist_ok=True, parents=True)
        for model_info in to_export:
            print(f"Start export {model_info.model_cls.__name__} data")
            resource = model_info.resource_cls()
            dataset = resource.export()
            with open(tmp_dir/model_info.file_name, "w", encoding="utf-8") as file:
                file.write(dataset.csv)
            print(f"End export {model_info.model_cls.__name__} data")

        print("Start export icons")
        icons_dir = tmp_dir/"icons"
        icons_dir.mkdir(exist_ok=True)
        for icon in Icon.objects.all():
            icon_path = icon.icon.path
            target_path = icons_dir/icon.icon.name
            if target_path.parent != icons_dir:
                target_path.parent.mkdir(exist_ok=True)
            shutil.copyfile(icon_path, target_path)
        print("End export icons")

        print("Start export maps")
        maps_dir = tmp_dir/"maps"
        maps_dir.mkdir(exist_ok=True)
        for location_map in LocationMapInfo.objects.all():
            map_path = location_map.map_image.path
            target_path = maps_dir/location_map.map_image.name
            if target_path.parent != maps_dir:
                target_path.parent.mkdir(exist_ok=True)
            shutil.copyfile(map_path, target_path)
        print("End export maps")
        shutil.make_archive('data', 'zip', tmp_dir)
        print("End archiving data")
        shutil.rmtree(tmp_dir)
