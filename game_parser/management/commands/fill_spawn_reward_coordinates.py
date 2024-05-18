import logging
import re
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import SpawnReward

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        coordinates_re_raw = (
            r"\s*xyz\(\s*(?P<x>[\d\.-]+),\s*(?P<y>[\d\.-]+),\s*(?P<z>[\d\.-]+)\s*\)\s*"
        )
        coordinates_re = re.compile(coordinates_re_raw)
        count = SpawnReward.objects.filter(
            x__isnull=True,
            xyz_raw__regex=coordinates_re_raw,
        ).count()
        for index, item in enumerate(
            SpawnReward.objects.filter(
                x__isnull=True,
                xyz_raw__regex=coordinates_re_raw,
            ),
        ):
            if rm := coordinates_re.match(item.xyz_raw):
                item.x = rm.group("x")
                item.y = rm.group("y")
                item.z = rm.group("z")
                item.save()
            if index % 100 == 0:
                print(f"{index + 1}/{count}")
