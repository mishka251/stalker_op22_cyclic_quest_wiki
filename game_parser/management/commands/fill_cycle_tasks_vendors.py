import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import GameStoryId, CycleTaskVendor

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = CycleTaskVendor.objects.count()
        for index, item in enumerate(CycleTaskVendor.objects.all()):
            item.game_story_id = GameStoryId.objects.filter(story_id=item.game_story_id_raw).first()
            item.save()
            print(f'{index+1}/{count}')

