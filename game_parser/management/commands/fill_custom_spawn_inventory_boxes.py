import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CustomSpawnItem, InventoryBox

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = CustomSpawnItem.objects.filter(section_name="inventory_box").count()
        for index, item in enumerate(CustomSpawnItem.objects.filter(section_name="inventory_box").all()):
            if not item.custom_data:
                continue
            item.custom_inventory_box = InventoryBox.objects.filter(source_file_name=f"config\{item.custom_data.strip()}").first()
            item.save()
            print(f'{index+1}/{count}')

