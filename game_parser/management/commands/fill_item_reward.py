import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import BaseItem, ItemReward

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = ItemReward.objects.count()
        for index, item in enumerate(ItemReward.objects.all()):
            item.item = BaseItem.objects.filter(name=item.raw_item).first()
            item.save()
            print(f"{index+1}/{count}")
