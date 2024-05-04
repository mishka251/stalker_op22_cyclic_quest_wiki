import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import GameTask, Translation

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = GameTask.objects.count()
        for index, item in enumerate(GameTask.objects.all()):
            item.title = Translation.objects.filter(code=item.title_id_raw).first()
            item.save()
            print(f"{index+1}/{count}")
