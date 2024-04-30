import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CycleTaskVendor, CyclicQuest

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        count = CyclicQuest.objects.count()
        for index, item in enumerate(CyclicQuest.objects.all()):
            item.vendor = CycleTaskVendor.objects.filter(vendor_id=int(item.giver_code_local)).first()
            item.giver_code_global = item.vendor.game_story_id_raw if item.vendor is not None else None
            item.save()
            print(f"{index+1}/{count}")

