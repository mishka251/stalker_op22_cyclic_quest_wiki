import re
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import GameVertex, Location

position_re = re.compile(r"\s*(?P<x>.*),\s*(?P<y>.*),\s*(?P<z>.*)")


class Command(BaseCommand):

    def get_file_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "spawns" / "graph.ltx"

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        GameVertex.objects.all().delete()

        parser = LtxParser(self.get_file_path())
        results = parser.get_parsed_blocks()

        vertexes = {
            vertex_id: vertex
            for vertex_id, vertex in results.items()
            if vertex_id.startswith("vertex")
        }
        vertexes_for_create = []
        for vertex_name, vertex in vertexes.items():
            if not isinstance(vertex, dict):
                raise TypeError
            vertex_id = int(vertex_name[len("vertex_") :])
            game_vertex = self._parse_vertex(vertex, vertex_id)
            vertexes_for_create.append(game_vertex)

        GameVertex.objects.bulk_create(vertexes_for_create, batch_size=2_000)

    def _parse_vertex(self, vertex: dict, vertex_id: int) -> GameVertex:
        level_point = vertex["level_point"]
        game_point = vertex["game_point"]
        if rm := position_re.match(level_point):
            level_point_x = rm.group("x")
            level_point_y = rm.group("y")
            level_point_z = rm.group("z")
        else:
            raise ValueError
        if rm := position_re.match(game_point):
            game_point_x = rm.group("x")
            game_point_y = rm.group("y")
            game_point_z = rm.group("z")
        else:
            raise ValueError
        return GameVertex(
            vertex_id=vertex_id,
            level_point_x=level_point_x,
            level_point_y=level_point_y,
            level_point_z=level_point_z,
            game_point_x=game_point_x,
            game_point_y=game_point_y,
            game_point_z=game_point_z,
            level_id_raw=vertex["level_id"],
            level_vertex_id=vertex["level_vertex_id"],
            vertex_type_raw=vertex["vertex_type"],
            level_points_raw=vertex["level_points"],
            edges_raw=vertex["edges"],
            location=Location.objects.filter(
                game_id=str(vertex["level_id"]).zfill(2).lower(),
            ).first(),
        )
