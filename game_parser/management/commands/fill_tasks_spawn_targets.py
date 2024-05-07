import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import CampInfo, CyclicQuest, SpawnItem, StalkerSection
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = CyclicQuest.objects.count()
        for index, item in enumerate(CyclicQuest.objects.all()):
            if not isinstance(item.target_str, str):
                raise TypeError
            if item.type == QuestKinds.KILL:
                item.target_stalker = StalkerSection.objects.filter(
                    section_name=item.target_str,
                ).first()
            elif item.type == QuestKinds.DEFEND_LAGER:
                item.target_camp_to_defeat = SpawnItem.objects.filter(
                    name=item.target_str,
                ).first()
                item.target_camp = CampInfo.objects.filter(
                    spawn_item__name=item.target_str,
                ).first()
            elif item.type == QuestKinds.DESTROY_CAMP:
                item.target_camp_to_destroy = SpawnItem.objects.filter(
                    name=item.target_str,
                ).first()
                item.target_camp = CampInfo.objects.filter(
                    spawn_item__name=item.target_str,
                ).first()
            else:
                continue
            item.save()
            print(f"{index + 1}/{count}")
