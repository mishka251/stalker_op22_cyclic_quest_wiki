import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import BaseItem, SpawnReward

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = SpawnReward.objects.count()
        for index, item in enumerate(SpawnReward.objects.all()):
            item.item = BaseItem.objects.filter(name=item.raw_maybe_item).first()
            item.save()
            print(f"{index+1}/{count}")
