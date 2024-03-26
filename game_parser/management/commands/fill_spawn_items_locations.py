import logging
import re

from django.core.management.base import BaseCommand
from django.db.models.functions import Lower
from django.db.transaction import atomic

from game_parser.models import Location
from game_parser.models import SpawnItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        location_name_re = re.compile(r"alife_(?P<location>.*)\.ltx")
        count = SpawnItem.objects.count()
        for index, item in enumerate(SpawnItem.objects.all()):
            if index % 100 == 0:
                print(f'{index+1:_}/{count:_}')
            match = location_name_re.match(item.location_txt)
            if not match:
                continue
            location_name = match.group("location")
            item.location = Location.objects.annotate(name_lower=Lower("name")).filter(name_lower=location_name.lower()).first()
            item.save()

