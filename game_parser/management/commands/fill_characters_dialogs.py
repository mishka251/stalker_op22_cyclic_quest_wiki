import logging
from typing import Optional

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import StorylineCharacter
from game_parser.models.game_story.dialog import Dialog

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        count = StorylineCharacter.objects.count()
        for index, item in enumerate(StorylineCharacter.objects.all()):
            item.dialogs.set(self._get_dialogs_by_raw(item.dialogs_raw))
            print(f"{index + 1}/{count}")

    def _get_dialogs_by_raw(self, raw: str | None) -> set[Dialog]:
        if raw is None:
            return set()
        values = raw.split(";")
        result = set()
        for dialog_id in values:
            if not dialog_id:
                continue
            dialog = Dialog.objects.filter(game_id=dialog_id).first()
            if dialog is not None:
                result.add(dialog)
            else:
                logger.warning(f"Dialog not found {dialog_id}")
        return result
