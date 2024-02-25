from lxml.etree import Element

from game_parser.logic.model_xml_loaders.base import BaseModelXmlLoader, TModel
from game_parser.models import GameTask, TaskObjective, MapLocationType


class GameTaskLoader(BaseModelXmlLoader[GameTask]):
    expected_tag = "game_task"
    def _load(self, game_task_node: Element, comments: list[str]) -> GameTask:
        # print(game_task_node)
        task_id = game_task_node.attrib.pop('id')
        prio = game_task_node.attrib.pop('prio', None)
        task = GameTask.objects.create(game_id=task_id, prio=prio)
        for child_node in game_task_node:
            # print(child_node)
            if child_node.tag == 'title':
                task.title_id_raw = child_node.text
            elif child_node.tag == 'objective':
                self._parse_task_objective(task, child_node)
            else:
                raise ValueError(f'Unexpected game task child {child_node.tag} in {task_id}')
        task.save()
        return task

    def _parse_task_objective(self, task: GameTask, objective_node: Element) -> None:
        # print(objective_node)
        # task_id = game_task_node.attrib.pop('id')
        # prio = game_task_node.attrib.pop('prio')
        # task = GameTask.objects.create(game_id=task_id, prio=prio)
        text = None
        icon = None
        infoportion_fails = []
        infoportion_completes = []
        infoportion_set_completes = []
        function_complete_raw = []
        function_fail_raw = []
        infoportion_set_fail_raw = []
        function_call_complete_raw = []
        article = None
        object_story_id = None

        map_location_types = []

        for child_node in objective_node:
            # print(child_node)
            if child_node.tag == 'text' and text is None:
                text = child_node.text
            elif child_node.tag == 'icon' and icon is None:
                icon = child_node.text
            elif child_node.tag == 'infoportion_fail':
                infoportion_fails.append(child_node.text)
                # if len(infoportion_fails) > 1:
                #     logger.debug(f'{len(infoportion_fails)=} in {task.game_id}')
            elif child_node.tag == 'infoportion_set_fail':
                infoportion_set_fail_raw.append(child_node.text)
            elif child_node.tag == 'function_call_complete':
                function_call_complete_raw.append(child_node.text)
            elif child_node.tag == 'function_fail':
                function_fail_raw.append(child_node.text)
                # if len(function_fail_raw) > 1:
                #     logger.debug(f'{len(function_fail_raw)=} in {task.game_id}')
            elif child_node.tag == 'infoportion_complete':
                infoportion_completes.append(child_node.text)
                # if len(infoportion_completes) > 1:
                #     logger.debug(f'{len(infoportion_completes)=} in {task.game_id}')
            elif child_node.tag == 'function_complete':
                function_complete_raw.append(child_node.text)
                # if len(function_complete_raw) > 1:
                #     logger.debug(f'{len(function_complete_raw)=} in {task.game_id}')
            elif child_node.tag == 'infoportion_set_complete':
                infoportion_set_completes.append(child_node.text)
                # if len(infoportion_set_completes) > 1:
                #     logger.debug(f'{len(infoportion_set_completes)=} in {task.game_id}')
            elif child_node.tag == 'article' and article is None:
                article = child_node.text
            elif child_node.tag == 'object_story_id' and object_story_id is None:
                object_story_id = child_node.text
            elif child_node.tag == 'map_location_type':
                map_location_type = {'name': child_node.text, 'hint': child_node.attrib.pop('hint', None)}
                map_location_types.append(map_location_type)
            elif child_node.tag == 'function_call_fail':
                print(f"Skip function_call_fail")
            else:
                raise ValueError(f'Unexpected objective child {child_node.tag} in {task.game_id}')
        objective = TaskObjective.objects.create(
            task=task,
            text_id_raw=text,
            icon_raw=icon,
            article_id_raw=article,
            infoportion_complete_raw=';'.join(infoportion_completes),
            infoportion_set_complete_raw=';'.join(infoportion_set_completes),
            function_complete_raw=';'.join(function_complete_raw),
            function_fail_raw=';'.join(function_fail_raw),
            object_story_id_raw=object_story_id,
            infoportion_set_fail_raw=';'.join(infoportion_set_fail_raw),
            function_call_complete_raw=';'.join(function_call_complete_raw),
        )

        for map_location_type in map_location_types:
            MapLocationType.objects.create(
                objective=objective,
                hint_raw=map_location_type['hint'],
                location_type=map_location_type['name'],
            )