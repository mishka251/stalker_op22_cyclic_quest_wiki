import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import QuestRandomReward, BaseItem, StalkerSection, StorylineCharacter, SingleStalkerSpawnItem, \
    Respawn, CyclicQuest
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = StalkerSection.objects.count()
        for index, item in enumerate(StalkerSection.objects.all()):
            item.character_profile = (
                StorylineCharacter.objects.filter(game_id__exact=item.character_profile_str.lower()).first()
                or StorylineCharacter.objects.filter(game_code__exact=item.character_profile_str.lower()).first()
            )
            item.save()
            if index % 100 == 0:
                print(f'{index+1}/{count}')

        count = SingleStalkerSpawnItem.objects.count()
        for index, item in enumerate(SingleStalkerSpawnItem.objects.all()):
            item.stalker_section = (
                StalkerSection.objects.filter(section_name__exact=item.character_profile_raw.lower()).first()
                or StalkerSection.objects.filter(character_profile_str__exact=item.character_profile_raw.lower()).first()
            )
            item.save()
            if index % 100 == 0:
                print(f'{index + 1}/{count}')

        count = Respawn.objects.count()
        for index, item in enumerate(Respawn.objects.all()):
            if not item.respawn_section_raw:
                continue
            respawn_sections = [s.strip() for s in item.respawn_section_raw.split(",")]
            stalkers = StalkerSection.objects.filter(section_name__in=respawn_sections)
            item.respawn_section.set(stalkers)
            # item.save()
            if index % 100 == 0:
                print(f'{index + 1}/{count}')

        count = CyclicQuest.objects.count()
        for index, item in enumerate(CyclicQuest.objects.all()):
            if item.type != QuestKinds.kill_stalker:
                continue
            item.target_stalker = (StalkerSection.objects.filter(section_name__exact=item.target_str.lower()).first()            )
            item.save()
            print(f'{index + 1}/{count}')
