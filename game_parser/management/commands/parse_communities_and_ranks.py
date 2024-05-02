import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import Community, CommunityType, Rank, RankType, Translation

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        print("Start cleaning")
        base_path = settings.OP22_GAME_DATA_PATH
        system_file = base_path / "config" / "system.ltx"

        Rank.objects.all().delete()
        Community.objects.all().delete()

        print("Cleaned")

        parser = LtxParser(system_file)
        results = parser.get_parsed_blocks()
        assert isinstance(results["game_relations"], dict)
        assert isinstance(results["monster_communities"], dict)
        stalker_ranks_raw = results["game_relations"]["rating"]
        monster_ranks_raw = results["game_relations"]["monster_rating"]

        stalker_communities = results["game_relations"]["communities"]
        monster_communities = results["monster_communities"]["communities"]

        self._parse_ranks(stalker_ranks_raw, RankType.STALKER)
        self._parse_ranks(monster_ranks_raw, RankType.MUTANT)

        self._parse_communities(stalker_communities, CommunityType.STALKER)
        self._parse_communities(monster_communities, CommunityType.MUTANT)
        print("OK")

    def _parse_ranks(self, raw_ranks: str, type_: RankType) -> None:
        ranks: list[Rank] = []
        for i, item_ in enumerate(raw_ranks.split(",")):
            item = item_.strip()
            if i % 2 == 0:
                rank = Rank(
                    name=item,
                    type=type_,
                    translation=Translation.objects.filter(code=item).first(),
                )
                ranks.append(rank)
                if i > 0:
                    rank.min_score = ranks[-1].max_score
            else:
                ranks[-1].max_score = int(item)
        Rank.objects.bulk_create(ranks)

    def _parse_communities(self, raw_communities: str, type_: CommunityType) -> None:
        communities: list[Community] = []
        for i, item_ in enumerate(raw_communities.split(",")):
            item = item_.strip()
            if i % 2 == 0:
                community = Community(
                    code=item,
                    type=type_,
                    translation=Translation.objects.filter(code=item).first(),
                )
                communities.append(community)
            else:
                communities[-1].index = int(item)
        Community.objects.bulk_create(communities)
