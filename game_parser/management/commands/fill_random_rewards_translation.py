import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, QuestRandomReward

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = QuestRandomReward.objects.count()
        for index, item in enumerate(QuestRandomReward.objects.all()):
            translation_id = f"task_item_type_{item.index}"
            item.name = translation_id
            item.name_translation = Translation.objects.filter(code__iexact=translation_id).first()
            item.save()
            print(f'{index+1}/{count}')

