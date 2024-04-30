import logging
from typing import Optional

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import InfoPortion, ScriptFunction
from game_parser.models.game_story.dialog import DialogPhrase, Dialog

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        count = DialogPhrase.objects.count()
        for index, item in enumerate(DialogPhrase.objects.all()):
            item.give_info.set(self._get_info_portions_by_raw(item.give_info_raw))
            item.actions.set(self._get_scripts_by_raw(item.actions_raw))
            item.precondition.set(self._get_scripts_by_raw(item.precondition_raw))
            item.has_info.set(self._get_info_portions_by_raw(item.has_info_raw))
            item.don_has_info.set(self._get_info_portions_by_raw(item.dont_has_info_raw))
            item.disable_info.set(self._get_info_portions_by_raw(item.disable_info_raw))
            item.disable.set(self._get_info_portions_by_raw(item.disable_raw))
            item.save()
            print(f"DialogPhrase:  {index + 1}/{count}")

        count = Dialog.objects.count()
        for index, item in enumerate(Dialog.objects.all()):
            item.has_info.set(self._get_info_portions_by_raw(item.has_info_raw))
            item.dont_has_info.set(self._get_info_portions_by_raw(item.dont_has_info_raw))
            item.give_info.set(self._get_info_portions_by_raw(item.give_info_raw))
            item.precondition.set(self._get_scripts_by_raw(item.precondition_raw))
            item.init_func.set(self._get_scripts_by_raw(item.init_func_raw))
            item.save()
            print(f"Dialog:  {index + 1}/{count}")

    def _get_scripts_by_raw(self, raw: Optional[str]) -> set[ScriptFunction]:
        if raw is None:
            return set()
        values = raw.split(";")
        result = set()
        for function_full_name in values:
            if not function_full_name:
                continue
            if "." in function_full_name:
                func_namespace, func_name = function_full_name.rsplit(".", 1)
                function = ScriptFunction.objects.filter(name=func_name, namespace=func_namespace).first()
            else:
                function = ScriptFunction.objects.filter(name=function_full_name).first()
            if function is not None:
                result.add(function)
            else:
                logger.warning(f"Function not found {function_full_name}")
        return result

    def _get_info_portions_by_raw(self, raw: Optional[str]) -> set[InfoPortion]:
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
