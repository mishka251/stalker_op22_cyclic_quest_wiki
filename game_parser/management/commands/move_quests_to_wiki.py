import re

from django.core.management import BaseCommand

from game_parser.models import CycleTaskVendor as ParserVendor
from game_parser.models import CyclicQuest as ParserCyclicQuest
from game_parser.models import Outfit as ParserOutfit
from game_parser.models import QuestRandomReward as ParserRandomReward
from game_parser.models import Silencer as ParserSilencer
from game_parser.models import SingleStalkerSpawnItem, SpawnItem
from game_parser.models import Weapon as ParserWeapon
from game_parser.models.quest import QuestKinds as ParserQuestKinds
from stalker_op22_cyclic_quest_wiki.models import Community as WikiCommunity
from stalker_op22_cyclic_quest_wiki.models import CycleTaskTargetItem, CycleTaskTargetCamp, \
    MapPosition, CycleTaskTargetStalker
from stalker_op22_cyclic_quest_wiki.models import CycleTaskVendor as WikiVendor
from stalker_op22_cyclic_quest_wiki.models import CyclicQuest as WikiQuest
from stalker_op22_cyclic_quest_wiki.models import Icon as WikiIcon
from stalker_op22_cyclic_quest_wiki.models import Item as WikiItem
from stalker_op22_cyclic_quest_wiki.models import ItemReward as WikiItemReward
from stalker_op22_cyclic_quest_wiki.models import Location as WikiLocation
from stalker_op22_cyclic_quest_wiki.models import MoneyReward as WikiMoneyReward
from stalker_op22_cyclic_quest_wiki.models import QuestRandomReward as WikiQuestRandomReward
from stalker_op22_cyclic_quest_wiki.models import RandomRewardInfo as WikiRandomReward
from stalker_op22_cyclic_quest_wiki.models import StalkerRank as WikiRank
from stalker_op22_cyclic_quest_wiki.models import Translation as WikiTranslation
from stalker_op22_cyclic_quest_wiki.models import TreasureReward as WikiTreasureReward


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        print("START")
        self._update_vendors()
        self._update_random_rewards()
        self._update_quests()
        print("END")

    def _update_vendors(self):
        print("start vendors")
        cnt = ParserVendor.objects.count()
        for i, vendor in enumerate(ParserVendor.objects.all()):
            profile = vendor.get_npc_profile()
            tmp = vendor.game_story_id
            name_translation = (
                WikiTranslation.objects.filter(code=profile.name_translation.code).first()
                if profile.name_translation
                else None
            )
            icon = (
                WikiIcon.objects.filter(name=profile.icon.name).first()
                if profile.icon
                else None
            )
            WikiVendor.objects.update_or_create(
                local_id=vendor.vendor_id,
                section_name=tmp.section_name,
                game_story_id=tmp.story_id,
                defaults={
                    "name_translation": name_translation,
                    "icon": icon,
                }
            )
            if i % 100 == 0:
                print(f"{i}/{cnt}")
        print("end vendors")

    def _update_random_rewards(self):
        print("start random rewards")
        cnt = ParserRandomReward.objects.count()
        for i, random_reward in enumerate(ParserRandomReward.objects.all()):
            name_translation = (
                WikiTranslation.objects.filter(code=random_reward.name_translation.code).first()
                if random_reward.name_translation
                else None
            )
            icon = (
                WikiIcon.objects.filter(name=random_reward.icon.name).first()
                if random_reward.icon
                else None
            )
            wiki_random_reward = WikiRandomReward.objects.update_or_create(
                index=random_reward.index,
                defaults={
                    "icon": icon,
                    "description": name_translation,
                },
            )[0]
            possible_items = [
                WikiItem.objects.get(name=item.name)
                for item in random_reward.possible_items.all()
            ]
            raw_count = len(random_reward.possible_items_str.split(";"))
            if raw_count != len(possible_items):
                raise ValueError(
                    f"Items not found. Expected: {random_reward.possible_items_str}, actual: {possible_items}")
            wiki_random_reward.possible_items.set(possible_items)
            if i % 100 == 0:
                print(f"{i}/{cnt}")
        print("end random rewards")

    def _update_quests(self):
        print("start quests")
        cnt = ParserCyclicQuest.objects.count()
        for i, quest in enumerate(ParserCyclicQuest.objects.all()):
            text_translation = (
                WikiTranslation.objects.filter(code=quest.text.code).first()
                if quest.text
                else None
            )

            vendor = (
                WikiVendor.objects.filter(local_id=quest.vendor.vendor_id).first()
                if quest.vendor
                else None
            )
            wiki_quest = WikiQuest.objects.update_or_create(
                game_code=quest.game_code,
                defaults={
                    "type": quest.type,
                    "prior": quest.prior,
                    "once": quest.once,
                    "vendor": vendor,
                    "text": text_translation,
                }
            )[0]
            self._update_quest_rewards(quest, wiki_quest)
            self._update_quest_target(quest, wiki_quest)
            if i % 100 == 0:
                print(f"{i}/{cnt}")
        print("end quests")

    def _update_quest_rewards(self, quest: ParserCyclicQuest, wiki_quest: WikiQuest) -> None:
        WikiMoneyReward.objects.filter(quest=wiki_quest).delete()
        if quest.reward_money is not None:
            WikiMoneyReward.objects.update_or_create(
                quest=wiki_quest,
                defaults={
                    "money": quest.reward_money,
                }
            )
        WikiTreasureReward.objects.filter(quest=wiki_quest).delete()
        if quest.reward_treasure:
            WikiTreasureReward.objects.update_or_create(quest=wiki_quest)
        WikiItemReward.objects.filter(quest=wiki_quest).delete()
        for item_reward in quest.item_rewards.all():
            wiki_item = WikiItem.objects.get(name=item_reward.item.name)
            WikiItemReward.objects.update_or_create(
                quest=wiki_quest,
                item=wiki_item,
                defaults={
                    "count": item_reward.count,
                }
            )
        WikiQuestRandomReward.objects.filter(quest=wiki_quest).delete()
        for random_reward in quest.random_rewards.all():
            reward = WikiRandomReward.objects.get(index=random_reward.reward.index)
            WikiQuestRandomReward.objects.update_or_create(
                quest=wiki_quest,
                reward=reward,
                defaults={
                    "count": random_reward.count,
                }
            )

    def _update_quest_target(self, quest: ParserCyclicQuest, wiki_quest: WikiQuest) -> None:
        item_target_quest_types = {
            ParserQuestKinds.chain,
            ParserQuestKinds.monster_part,
            ParserQuestKinds.artefact,
            ParserQuestKinds.find_item,
        }

        camp_target_quest_types = {
            ParserQuestKinds.eliminate_lager,
            ParserQuestKinds.defend_lager,
        }
        stalker_target_quest_types = {
            ParserQuestKinds.kill_stalker,
        }

        if quest.type in item_target_quest_types:
            wiki_item = WikiItem.objects.get(name=quest.target_item.name)
            target_cond_str = quest.target_cond_str
            items_with_condition = (ParserWeapon, ParserOutfit, ParserSilencer)
            if target_cond_str is None and isinstance(quest.target_item, items_with_condition):
                target_cond_str = "50"
            CycleTaskTargetItem.objects.update_or_create(
                quest=wiki_quest,
                defaults={
                    "item": wiki_item,
                    "count": quest.target_count,
                    "cond_str": target_cond_str,
                }
            )
        elif quest.type in camp_target_quest_types:
            target_camp = quest.target_camp
            communities_raw = [s.strip() for s in (target_camp.communities_raw or "").split(",")]
            print(communities_raw)
            communities = [
                WikiCommunity.objects.filter(name=community).first()
                for community in communities_raw
            ]
            communities = [
                community
                for community in communities
                if community is not None
            ]
            map_position = self._spawn_item_to_map_position(quest.target_camp.spawn_item)
            camp = CycleTaskTargetCamp.objects.update_or_create(
                quest=wiki_quest,
                defaults={
                    "map_position": map_position,
                }
            )[0]
            camp.communities.set(communities)
        elif quest.type in stalker_target_quest_types:
            community = WikiCommunity.objects.get(name=quest.target_stalker.community_str)
            rank = WikiRank.objects.get(name=quest.target_stalker.spec_rank_str)
            stalker = CycleTaskTargetStalker.objects.update_or_create(
                quest=wiki_quest,
                defaults={
                    "rank": rank,
                    "community": community,
                }
            )[0]
            single_spawn_items = SingleStalkerSpawnItem.objects.filter(stalker_section=quest.target_stalker)
            single_spawn_items_ids = single_spawn_items.values_list("spawn_item_id", flat=True)
            respawns = quest.target_stalker.respawn_set.all()
            respawns_spawn_items = respawns.values_list("spawn_item_id", flat=True)
            possible_spawn_items = SpawnItem.objects.filter(
                id__in=list(single_spawn_items_ids) + list(respawns_spawn_items)
            )
            map_positions = [
                self._spawn_item_to_map_position(spawn_item)
                for spawn_item in possible_spawn_items
            ]
            stalker.map_positions.set(map_positions)
        else:
            raise ValueError(f"Неизвестный вид квеста {quest.type}")

    def _spawn_item_to_map_position(self, spawn_item: SpawnItem) -> MapPosition:
        location = WikiLocation.objects.get(name=spawn_item.location.name)
        position_re = re.compile(r"\s*(?P<x>.*),\s*(?P<y>.*),\s*(?P<z>.*)")
        rm = position_re.match(spawn_item.position_raw)
        (x, y, z) = float(rm.group("x")), float(rm.group("y")), float(rm.group("z"))
        map_position = MapPosition.objects.update_or_create(
            spawn_id=spawn_item.spawn_id,
            story_id=spawn_item.story_id,
            spawn_story_id=spawn_item.spawn_story_id,
            defaults={
                "name": spawn_item.name,
                "x": x,
                "y": y,
                "z": z,
                "game_vertex_id": spawn_item.game_vertex_id,
                "location": location,
            }
        )[0]

        return map_position
