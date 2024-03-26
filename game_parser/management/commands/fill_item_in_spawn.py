import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import BaseItem, SpawnItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = SpawnItem.objects.count()
        for index, item in enumerate(SpawnItem.objects.all()):
            item.item = (
                BaseItem.objects.filter(name=item.section_name).first()
                or BaseItem.objects.filter(inv_name=item.section_name).first()
            )
            item.save()
            print(f'{index+1:_}/{count:_}')

