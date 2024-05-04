import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import BaseItem, ItemInTreasure, Treasure

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        treasures_count = Treasure.objects.count()
        for index, treasure in enumerate(Treasure.objects.all()):
            items_names_or_counts: list[str] = [
                s.strip() for s in treasure.items_str.split(",")
            ]
            prev_item_name = None

            for item_name_or_count in items_names_or_counts:
                if item_name_or_count.isdigit():
                    count = int(item_name_or_count)
                    if prev_item_name is None:
                        raise ValueError(
                            f"{count=}, {prev_item_name=}, {treasure.items_str=}",
                        )
                    try:
                        item = BaseItem.objects.get(name=prev_item_name)
                        ItemInTreasure.objects.create(
                            count=count,
                            item=item,
                            treasure=treasure,
                        )
                    except BaseItem.DoesNotExist:
                        logger.warning(f'"{prev_item_name}" not found')

                    prev_item_name = None
                else:
                    if prev_item_name is not None:
                        try:
                            item = BaseItem.objects.get(name=prev_item_name)
                            ItemInTreasure.objects.create(
                                item=item,
                                treasure=treasure,
                            )
                        except BaseItem.DoesNotExist:
                            logger.warning(f'"{prev_item_name}" not found')
                    prev_item_name = item_name_or_count

            print(f"{index + 1}/{treasures_count}")
