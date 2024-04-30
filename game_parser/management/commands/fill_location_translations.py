import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Location
from game_parser.models import Translation

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = Location.objects.count()
        for index, item in enumerate(Location.objects.all()):
            item.name_translation = Translation.objects.filter(code__iexact=item.name.lower()).first()
            item.save()
            print(f"{index+1}/{count}")

