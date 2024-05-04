import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import BaseItem, GameStoryId, StorylineCharacter, Treasure

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = GameStoryId.objects.count()
        for index, item in enumerate(GameStoryId.objects.all()):
            section_name = item.section_name.lower()
            item.item = (
                BaseItem.objects.filter(name__iexact=section_name).first()
                or BaseItem.objects.filter(inv_name__iexact=section_name).first()
            )
            item.treasure = Treasure.objects.filter(
                name_str__iexact=section_name,
            ).first()
            item.character = StorylineCharacter.objects.filter(
                game_id__iexact=section_name,
            ).first()
            item.save()
            print(f"{index+1}/{count}")
