import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.models.functions import Lower
from django.db.transaction import atomic

from game_parser.models import Location, LocationMapInfo

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = LocationMapInfo.objects.count()
        locations = Location.objects.annotate(name_lower=Lower("name"))
        for index, item in enumerate(LocationMapInfo.objects.all()):
            if item.name is None:
                continue
            item.location = locations.filter(
                name_lower=item.name,
            ).first()
            item.save()
            print(f"{index+1}/{count}")
