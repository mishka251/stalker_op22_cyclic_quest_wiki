from pathlib import Path
from xml.etree.ElementTree import Element, parse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

import logging

import re

from game_parser.logic.gsc_xml_fixer import GSCXmlFixer
from game_parser.models import GameTask, TaskObjective, MapLocationType

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / 'config'/'gameplay'

    def get_files_paths(self, path: Path) -> list[Path]:
        paths = []
        for path in path.iterdir():
            if path.name.startswith('tasks'):
                paths.append(path)
        # for (dir, _, files) in os.walk(path):
        #     for file_name in files:
        #         paths.append(Path(os.path.join(dir, file_name)))

        return paths

    @atomic
    def handle(self, **options):
        GameTask.objects.all().delete()
        TaskObjective.objects.all().delete()

        for file_path in self.get_files_paths(self.get_files_dir_path()):
            print(file_path)
            fixer = GSCXmlFixer(file_path)
            fixed_file_path = fixer.fix(add_root_tag=True)
            with open(fixed_file_path, 'r') as tml_file:
                root_node = parse(tml_file).getroot()
            # print(root_node)
            for game_task in root_node:
                if game_task.tag == 'game_task':
                    self._parse_game_task(game_task)
                else:
                    logger.warning(f'Unexpected node {game_task.tag} in {file_path}')

    def _parse_game_task(self, game_task_node: Element) -> None:
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
                logger.warning(f'Unexpected game task child {child_node.tag} in {task_id}')
        task.save()

    def _parse_task_objective(self, task: GameTask, objective_node: Element) -> None:
        # print(objective_node)
        # task_id = game_task_node.attrib.pop('id')
        # prio = game_task_node.attrib.pop('prio')
        # task = GameTask.objects.create(game_id=task_id, prio=prio)
        text = None
        icon=None
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
            else:
                logger.warning(f'Unexpected objective child {child_node.tag} in {task.game_id}')
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