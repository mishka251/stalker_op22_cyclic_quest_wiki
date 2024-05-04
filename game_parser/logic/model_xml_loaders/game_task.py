from lxml.etree import _Element

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader
from game_parser.models import GameTask, MapLocationType, TaskObjective


class GameTaskLoader(BaseModelXmlLoader[GameTask]):
    expected_tag = "game_task"

    def _load(self, game_task_node: _Element, comments: list[str]) -> GameTask:
        task_id = game_task_node.attrib.pop("id")
        prio = game_task_node.attrib.get("prio")
        task = GameTask.objects.create(game_id=task_id, prio=prio)
        for child_node in game_task_node:
            if child_node.tag == "title" and child_node.text is not None:
                task.title_id_raw = child_node.text
            elif child_node.tag == "objective":
                self._parse_task_objective(task, child_node)
            else:
                raise ValueError(
                    f"Unexpected game task child {child_node.tag} in {task_id}",
                )
        task.save()
        return task

    def _parse_task_objective(self, task: GameTask, objective_node: _Element) -> None:
        text = None
        icon = None
        infoportion_fails: list[str] = []
        infoportion_completes: list[str] = []
        infoportion_set_completes: list[str] = []
        function_complete_raw: list[str] = []
        function_fail_raw: list[str] = []
        infoportion_set_fail_raw: list[str] = []
        function_call_complete_raw: list[str] = []
        article = None
        object_story_id = None

        map_location_types = []

        for child_node in objective_node:
            if child_node.tag == "text" and text is None and child_node.text:
                text = child_node.text
            elif child_node.tag == "icon" and icon is None and child_node.text:
                icon = child_node.text
            elif child_node.tag == "infoportion_fail" and child_node.text:
                infoportion_fails.append(child_node.text)
            elif child_node.tag == "infoportion_set_fail" and child_node.text:
                infoportion_set_fail_raw.append(child_node.text)
            elif child_node.tag == "function_call_complete" and child_node.text:
                function_call_complete_raw.append(child_node.text)
            elif child_node.tag == "function_fail" and child_node.text:
                function_fail_raw.append(child_node.text)
            elif child_node.tag == "infoportion_complete" and child_node.text:
                infoportion_completes.append(child_node.text)
            elif child_node.tag == "function_complete" and child_node.text:
                function_complete_raw.append(child_node.text)
            elif child_node.tag == "infoportion_set_complete" and child_node.text:
                infoportion_set_completes.append(child_node.text)
            elif child_node.tag == "article" and article is None and child_node.text:
                article = child_node.text
            elif (
                child_node.tag == "object_story_id"
                and object_story_id is None
                and child_node.text
            ):
                object_story_id = child_node.text
            elif child_node.tag == "map_location_type":
                map_location_type = {
                    "name": child_node.text,
                    "hint": child_node.attrib.get("hint"),
                }
                map_location_types.append(map_location_type)
            elif child_node.tag == "function_call_fail":
                print("Skip function_call_fail")
            else:
                raise ValueError(
                    f"Unexpected objective child {child_node.tag} in {task.game_id}",
                )
        objective = TaskObjective.objects.create(
            task=task,
            text_id_raw=text,
            icon_raw=icon,
            article_id_raw=article,
            infoportion_complete_raw=";".join(infoportion_completes),
            infoportion_set_complete_raw=";".join(infoportion_set_completes),
            function_complete_raw=";".join(function_complete_raw),
            function_fail_raw=";".join(function_fail_raw),
            object_story_id_raw=object_story_id,
            infoportion_set_fail_raw=";".join(infoportion_set_fail_raw),
            function_call_complete_raw=";".join(function_call_complete_raw),
        )

        for map_location_type in map_location_types:
            assert map_location_type["name"] is not None
            MapLocationType.objects.create(
                objective=objective,
                hint_raw=map_location_type["hint"],
                location_type=map_location_type["name"],
            )
