import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import (
    CyclicQuest,
    Respawn,
    SingleStalkerSpawnItem,
    StalkerSection,
    StorylineCharacter,
)
from game_parser.models.quest import QuestKinds

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = StalkerSection.objects.count()
        for index, stalker_section in enumerate(StalkerSection.objects.all()):
            if stalker_section.character_profile_str is None:
                continue
            stalker_section.character_profile = (
                StorylineCharacter.objects.filter(
                    game_id__exact=stalker_section.character_profile_str.lower(),
                ).first()
                or StorylineCharacter.objects.filter(
                    game_code__exact=stalker_section.character_profile_str.lower(),
                ).first()
            )
            stalker_section.save()
            if index % 100 == 0:
                print(f"{index+1}/{count}")

        count = SingleStalkerSpawnItem.objects.count()
        for index, stalker_spawn_item in enumerate(
            SingleStalkerSpawnItem.objects.all(),
        ):
            stalker_spawn_item.stalker_section = (
                StalkerSection.objects.filter(
                    section_name__exact=stalker_spawn_item.character_profile_raw.lower(),
                ).first()
                or StalkerSection.objects.filter(
                    character_profile_str__exact=stalker_spawn_item.character_profile_raw.lower(),
                ).first()
            )
            stalker_spawn_item.save()
            if index % 100 == 0:
                print(f"{index + 1}/{count}")

        count = Respawn.objects.count()
        for index, respawn in enumerate(Respawn.objects.all()):
            if not respawn.respawn_section_raw:
                continue
            respawn_sections = [
                s.strip() for s in respawn.respawn_section_raw.split(",")
            ]
            stalkers = StalkerSection.objects.filter(section_name__in=respawn_sections)
            respawn.respawn_section.set(stalkers)
            if index % 100 == 0:
                print(f"{index + 1}/{count}")

        count = CyclicQuest.objects.count()
        for index, quest in enumerate(CyclicQuest.objects.all()):
            if quest.target_str is None:
                raise ValueError
            if quest.type != QuestKinds.KILL:
                continue
            quest.target_stalker = StalkerSection.objects.filter(
                section_name__exact=quest.target_str.lower(),
            ).first()
            quest.save()
            print(f"{index + 1}/{count}")
