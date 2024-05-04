import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, Treasure

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        count = Treasure.objects.count()
        for index, item in enumerate(Treasure.objects.all()):
            item.description_translation = Translation.objects.filter(
                code__iexact=item.description_str.lower(),
            ).first()
            if item.custom_name:
                item.custom_name_translation = Translation.objects.filter(
                    code__iexact=item.custom_name.lower(),
                ).first()
            item.save()
            print(f"{index+1}/{count}")
