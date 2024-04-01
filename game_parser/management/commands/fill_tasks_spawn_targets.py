import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CyclicQuest, SpawnItem, CampInfo
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = CyclicQuest.objects.count()
        for index, item in enumerate(CyclicQuest.objects.all()):
            if item.type == QuestKinds.kill_stalker:
                item.target_stalker = SpawnItem.objects.filter(name=item.target_str).first()
            elif item.type == QuestKinds.defend_lager:
                item.target_camp_to_defeat = SpawnItem.objects.filter(name=item.target_str).first()
                item.target_camp = CampInfo.objects.filter(spawn_item__name=item.target_str).first()
            elif item.type == QuestKinds.eliminate_lager:
                item.target_camp_to_destroy = SpawnItem.objects.filter(name=item.target_str).first()
                item.target_camp = CampInfo.objects.filter(spawn_item__name=item.target_str).first()
            else:
                continue
            item.save()
            print(f'{index + 1}/{count}')
