import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, CyclicQuest

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = CyclicQuest.objects.count()
        for index, item in enumerate(CyclicQuest.objects.all()):
            item.text_raw = f"tm_{item.game_code}_text"
            item.text = Translation.objects.filter(code=item.text_raw).first()
            item.save()
            print(f'{index + 1}/{count}')
