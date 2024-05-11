import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.transaction import atomic

from game_parser.models import Translation
from game_parser.models.items.base_item import BaseItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = BaseItem.objects.filter(
            Q(description_translation__isnull=True) | Q(name_translation__isnull=True),
        ).count()
        for index, item in enumerate(
            BaseItem.objects.filter(
                Q(description_translation__isnull=True)
                | Q(name_translation__isnull=True),
            ),
        ):

            item.description_translation = Translation.objects.filter(
                code=item.description_code,
            ).first()
            item.name_translation = Translation.objects.filter(
                code=item.inv_name,
            ).first()
            item.save()
            print(f"{index+1}/{count}")
