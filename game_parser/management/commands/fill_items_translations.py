import logging
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation
from game_parser.models.items.base_item import BaseItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = BaseItem.objects.count()
        for index, item in enumerate(BaseItem.objects.all()):
            item.description_translation = Translation.objects.filter(code=item.description_code).first()
            item.name_translation = Translation.objects.filter(code=item.inv_name).first()
            item.save()
            print(f'{index+1}/{count}')

