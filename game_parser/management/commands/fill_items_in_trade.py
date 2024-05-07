import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import ItemInTradeBase
from game_parser.models.items.base_item import BaseItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = ItemInTradeBase.objects.count()
        for index, item in enumerate(ItemInTradeBase.objects.all()):
            item.item = (
                BaseItem.objects.filter(name=item.item_name).first()
                or BaseItem.objects.filter(inv_name=item.item_name).first()
            )
            item.save()
            print(f"{index+1}/{count}")

        unfounded_items = set(
            ItemInTradeBase.objects.filter(item__isnull=True).values_list(
                "item_name",
                flat=True,
            ),
        )

        print(f"Not found = {unfounded_items}")
