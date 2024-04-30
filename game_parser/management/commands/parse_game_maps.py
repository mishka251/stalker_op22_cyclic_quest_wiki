import logging
from pathlib import Path

from PIL import Image
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db.models.functions import Lower
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import LocationMapInfo, Location

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "game_maps_single.ltx"

    def get_base_image(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "textures"

    @atomic
    def handle(self, **options):
        LocationMapInfo.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        locations_list = [
            level_name.lower()
            for level_name in results["level_maps_single"]
        ]

        results_lower = {
            key.lower(): value
            for key, value in results.items()
        }

        for level_name in locations_list:
            location_data = results_lower[level_name]
            print(location_data)

            location = LocationMapInfo.objects.create(
                name=level_name,
                location=Location.objects.annotate(lower_name=Lower("name")).filter(lower_name=level_name).first(),
                texture_raw=location_data.get("texture"),
                bound_rect_raw=location_data.get("bound_rect"),
                global_rect_raw=location_data.get("global_rect"),
                weathers=location_data.get("weathers"),
                music_tracks=location_data.get("music_tracks"),
            )
            if not location.texture_raw:
                continue
            image_path = self.get_base_image() / (location_data["texture"] + ".dds")
            image = Image.open(image_path)
            tmp_file_name = "tmp.png"
            image.save(tmp_file_name)
            with open(tmp_file_name, "rb") as tmp_image:
                image_file = ImageFile(tmp_image, name=level_name+ ".png")
                location.map_image = image_file
                location.save()

