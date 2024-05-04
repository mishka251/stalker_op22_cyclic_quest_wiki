import logging
from typing import Optional

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import InfoPortion, ScriptFunction
from game_parser.models.game_story.dialog import Dialog, DialogPhrase

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        count = DialogPhrase.objects.count()
        for index, dialog_phrase in enumerate(DialogPhrase.objects.all()):
            dialog_phrase.give_info.set(
                self._get_info_portions_by_raw(dialog_phrase.give_info_raw),
            )
            dialog_phrase.actions.set(
                self._get_scripts_by_raw(dialog_phrase.actions_raw),
            )
            dialog_phrase.precondition.set(
                self._get_scripts_by_raw(dialog_phrase.precondition_raw),
            )
            dialog_phrase.has_info.set(
                self._get_info_portions_by_raw(dialog_phrase.has_info_raw),
            )
            dialog_phrase.don_has_info.set(
                self._get_info_portions_by_raw(dialog_phrase.dont_has_info_raw),
            )
            dialog_phrase.disable_info.set(
                self._get_info_portions_by_raw(dialog_phrase.disable_info_raw),
            )
            dialog_phrase.disable.set(
                self._get_info_portions_by_raw(dialog_phrase.disable_raw),
            )
            dialog_phrase.save()
            print(f"DialogPhrase:  {index + 1}/{count}")

        count = Dialog.objects.count()
        for index, dialog in enumerate(Dialog.objects.all()):
            dialog.has_info.set(self._get_info_portions_by_raw(dialog.has_info_raw))
            dialog.dont_has_info.set(
                self._get_info_portions_by_raw(dialog.dont_has_info_raw),
            )
            dialog.give_info.set(self._get_info_portions_by_raw(dialog.give_info_raw))
            dialog.precondition.set(self._get_scripts_by_raw(dialog.precondition_raw))
            dialog.init_func.set(self._get_scripts_by_raw(dialog.init_func_raw))
            dialog.save()
            print(f"Dialog:  {index + 1}/{count}")

    def _get_scripts_by_raw(self, raw: str | None) -> set[ScriptFunction]:
        if raw is None:
            return set()
        values = raw.split(";")
        result = set()
        for function_full_name in values:
            if not function_full_name:
                continue
            if "." in function_full_name:
                func_namespace, func_name = function_full_name.rsplit(".", 1)
                function = ScriptFunction.objects.filter(
                    name=func_name,
                    namespace=func_namespace,
                ).first()
            else:
                function = ScriptFunction.objects.filter(
                    name=function_full_name,
                ).first()
            if function is not None:
                result.add(function)
            else:
                logger.warning(f"Function not found {function_full_name}")
        return result

    def _get_info_portions_by_raw(self, raw: str | None) -> set[InfoPortion]:
        if raw is None:
            return set()
        values = raw.split(";")
        result = set()
        for portion_id in values:
            if not portion_id:
                continue
            portion = InfoPortion.objects.filter(game_id=portion_id).first()
            if portion is not None:
                result.add(portion)
            else:
                logger.warning(f"InfoPortion not found {portion_id}")
        return result
