import logging

from django.core.management.base import BaseCommand
from django.db.models import Value
from django.db.models.functions import Concat
from django.db.transaction import atomic

from game_parser.models import TaskObjective, ScriptFunction, InfoPortion

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = TaskObjective.objects.count()
        functions = ScriptFunction.objects.all().annotate(fullname=Concat("namespace", Value("."), "name"))
        for index, item in enumerate(TaskObjective.objects.all()):
            if item.function_complete_raw and not item.function_complete:
                item.function_complete = functions.filter(fullname=item.function_complete_raw).first()
            if item.infoportion_complete_raw:
                item.infoportion_complete = InfoPortion.objects.filter(game_id=item.infoportion_complete_raw).first()
            if item.infoportion_set_complete_raw:
                item.infoportion_set_complete = InfoPortion.objects.filter(game_id=item.infoportion_set_complete_raw).first()
            if item.function_fail_raw and not item.function_fail:
                item.function_fail = functions.filter(fullname=item.function_fail_raw).first()
            if item.infoportion_set_fail_raw:
                item.infoportion_set_fail = InfoPortion.objects.filter(game_id=item.infoportion_set_fail_raw).first()
            if item.function_call_complete_raw and not item.function_call_complete:
                item.function_call_complete = functions.filter(fullname=item.function_call_complete_raw).first()

            item.save()
            print(f"{index + 1}/{count}")
