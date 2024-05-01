import re

from django.core.management import BaseCommand

from game_parser.models import Community as ParserCommunity
from game_parser.models import Icon as ParserIcon
from game_parser.models import Location as ParserLocation
from game_parser.models import LocationMapInfo as ParserLocationMapInfo
from game_parser.models import Rank as ParserRank
from game_parser.models import Translation as ParserTranslation
from stalker_op22_cyclic_quest_wiki.models import Community as WikiCommunity
from stalker_op22_cyclic_quest_wiki.models import Icon as WikiIcon
from stalker_op22_cyclic_quest_wiki.models import Location as WikiLocation
from stalker_op22_cyclic_quest_wiki.models import LocationMapInfo as WikiLocationMapInfo
from stalker_op22_cyclic_quest_wiki.models import StalkerRank as WikiRank
from stalker_op22_cyclic_quest_wiki.models import Translation as WikiTranslation


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print("START")
        self._update_translation()
        self._update_icons()
        self._update_communities()
        self._update_ranks()
        self._update_locations()
        print("END")

    def _update_translation(self):
        print("start translations")
        cnt = ParserTranslation.objects.count()
        for i, translation in enumerate(ParserTranslation.objects.all()):
            WikiTranslation.objects.update_or_create(
                code=translation.code,
                defaults={
                    "rus": translation.rus,
                    "eng": translation.eng,
                    "ukr": translation.ukr,
                    "pln": translation.pln,
                    "fra": translation.fra,
                },
            )
            if i % 100 == 0:
                print(f"{i}/{cnt}")
        print("end translations")

    def _update_icons(self):
        print("start icons")
        cnt = ParserIcon.objects.count()
        for i, translation in enumerate(ParserIcon.objects.all()):
            WikiIcon.objects.update_or_create(
                name=translation.name,
                defaults={
                    "icon": translation.icon,
                },
            )
            if i % 100 == 0:
                print(f"{i}/{cnt}")
        print("end icons")

    def _update_communities(self):
        print("start communities")
        for translation in ParserCommunity.objects.filter(translation__isnull=False):
            if translation.translation is None:
                continue
            WikiCommunity.objects.update_or_create(
                name=translation.code,
                defaults={
                    "translation": WikiTranslation.objects.get(
                        code=translation.translation.code
                    ),
                },
            )
        print("end communities")

    def _update_ranks(self):
        print("start ranks")
        for translation in ParserRank.objects.filter(translation__isnull=False):
            if translation.translation is None:
                continue
            WikiRank.objects.update_or_create(
                name=translation.name,
                defaults={
                    "translation": WikiTranslation.objects.get(
                        code=translation.translation.code
                    ),
                },
            )
        print("end ranks")

    def _update_locations(self):
        offset_re = re.compile(
            r"\s*(?P<min_x>.*),\s*(?P<min_y>.*),\s*(?P<max_x>.*),\s*(?P<max_y>.*)"
        )
        for parser_location in ParserLocation.objects.all():
            wiki_location_map_info = None
            parser_location_map_info = ParserLocationMapInfo.objects.filter(
                location=parser_location
            ).first()
            if (
                parser_location_map_info
                and parser_location_map_info.map_image
                and parser_location_map_info.bound_rect_raw
                and (rm := offset_re.match(parser_location_map_info.bound_rect_raw))
            ):

                (min_x, min_y, max_x, max_y) = (
                    float(rm.group("min_x")),
                    float(rm.group("min_y")),
                    float(rm.group("max_x")),
                    float(rm.group("max_y")),
                )

                wiki_location_map_info = WikiLocationMapInfo.objects.update_or_create(
                    location_name=parser_location.name,
                    defaults={
                        "map_image": parser_location_map_info.map_image,
                        "min_x": min_x,
                        "min_y": min_y,
                        "max_x": max_x,
                        "max_y": max_y,
                    },
                )[0]

            WikiLocation.objects.update_or_create(
                name=parser_location.name,
                defaults={
                    "name_translation": (
                        WikiTranslation.objects.filter(
                            code=parser_location.name_translation.code
                        ).first()
                        if parser_location.name_translation is not None
                        else None
                    ),
                    "map_info": wiki_location_map_info,
                },
            )
