import logging
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Translation, ItemReward, BaseItem, GameStoryId, StorylineCharacter, Treasure, \
    CyclicQuest, SpawnItem, TaskObjective, ScriptFunction, InfoPortion
from game_parser.models import GameTask
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = TaskObjective.objects.count()
        for index, item in enumerate(TaskObjective.objects.all()):
            if item.function_complete_raw:
                item.function_complete = ScriptFunction.objects.filter(name=item.function_complete_raw).first()
            if item.infoportion_complete_raw:
                item.infoportion_complete = InfoPortion.objects.filter(game_id=item.infoportion_complete_raw).first()
            if item.infoportion_set_complete_raw:
                item.infoportion_set_complete = InfoPortion.objects.filter(game_id=item.infoportion_set_complete_raw).first()
            if item.function_fail_raw:
                item.function_fail = ScriptFunction.objects.filter(name=item.function_fail_raw).first()
            if item.infoportion_set_fail_raw:
                item.infoportion_set_fail = InfoPortion.objects.filter(game_id=item.infoportion_set_fail_raw).first()
            if item.function_call_complete_raw:
                item.function_call_complete = ScriptFunction.objects.filter(name=item.function_call_complete_raw).first()

            item.save()
            print(f'{index + 1}/{count}')
