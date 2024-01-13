import logging
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, QuestRandomReward, BaseItem
from game_parser.models import GameTask

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = QuestRandomReward.objects.count()
        for index, item in enumerate(QuestRandomReward.objects.all()):
            raw_items = item.possible_items_str.split(';')
            item.possible_items.set(BaseItem.objects.filter(name__in=raw_items))
            if len(raw_items) != item.possible_items.count():
                print(f'warn {len(raw_items)=} != {item.possible_items.count()=}')
            print(f'{index+1}/{count}')
