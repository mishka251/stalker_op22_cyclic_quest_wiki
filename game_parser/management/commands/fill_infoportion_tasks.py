import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import GameTask, InfoPortion

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = InfoPortion.objects.count()
        for index, item in enumerate(InfoPortion.objects.all()):
            item.task = GameTask.objects.filter(game_id=item.task_raw).first()
            item.save()
            print(f"{index+1}/{count}")
