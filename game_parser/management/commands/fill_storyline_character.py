import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, StorylineCharacter, Icon

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = StorylineCharacter.objects.count()
        for index, item in enumerate(StorylineCharacter.objects.all()):
            item.name_translation = Translation.objects.filter(code__iexact=item.name_raw.lower()).first()
            item.icon = Icon.objects.filter(name__iexact=item.icon_raw.lower()).first()
            item.save()
            print(f"{index+1}/{count}")

