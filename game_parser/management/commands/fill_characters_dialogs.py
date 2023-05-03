import logging
from typing import Optional

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.db.models import QuerySet

from game_parser.models import Translation, InfoPortion, ScriptFunction, StorylineCharacter
from game_parser.models.game_story.dialog import DialogPhrase, Dialog
from game_parser.models.items.base_item import BaseItem

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = StorylineCharacter.objects.count()
        for index, item in enumerate(StorylineCharacter.objects.all()):
            item.dialogs.set(self._get_dialogs_by_raw(item.dialogs_raw))
            print(f'{index + 1}/{count}')

    def _get_dialogs_by_raw(self, raw: Optional[str]) -> set[Dialog]:
        if raw is None:
            return set()
        values = raw.split(';')
        result = set()
        for dialog_id in values:
            if not dialog_id:
                continue
            dialog = Dialog.objects.filter(game_id=dialog_id).first()
            if dialog is not None:
                result.add(dialog)
            else:
                logger.warning(f'Dialog not found {dialog_id}')
        return result
