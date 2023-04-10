import logging
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation
from game_parser.models.game_story.dialog import DialogPhrase
from game_parser.models.items.base_item import BaseItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = DialogPhrase.objects.count()
        for index, item in enumerate(DialogPhrase.objects.all()):
            item.text = Translation.objects.filter(code=item.text_id_raw).first()
            item.save()
            print(f'{index+1}/{count}')

