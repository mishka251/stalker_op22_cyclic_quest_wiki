import dataclasses
import decimal
import logging
import os
from pathlib import Path
from typing import Any, Callable, Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from luaparser.ast import ASTVisitor, Call, Function, Index, Invoke, Name, Nil, Number, Op, String, UnaryOp, parse, to_lua_source

from game_parser.models import ItemReward, MoneyReward, ScriptFunction, SpawnReward

logger = logging.getLogger(__name__)

def log_parse_error(func: Callable[[Any,Any], None]) -> Callable[[Any,Any], None]:
    def wrapper(self, node) -> None:
        try:
            func(self, node)
        except Exception as ex:
            logger.error(f"Ошибка при парсинге {to_lua_source(node)}")
            logger.exception(ex)
            raise
    return wrapper

@dataclasses.dataclass
class ItemRewardDto:
    item_name: str
    count: int

@dataclasses.dataclass
class SpawnDto:
    item_or_npc_name: str
    x: float
    y: float
    z: float
    level_vertex: int
    game_vertex_id: int
    raw: str
    xyz_raw: str
    target: str | None = None


class NestedCallsVisitor(ASTVisitor):
    def __init__(self):
        super().__init__()
        self._money_rewards = []
        self._item_rewards = []
        self._nested_calls = []
        self._spawn_rewards = []

    @log_parse_error
    def visit_Call(self, node: Call) -> None:
        node_func = node.func

        if isinstance(node.func, Call):
            return
        if isinstance(node_func, Index):
            func_name = to_lua_source(node_func)
        else:
            func_name = node_func.id

        if func_name == "got":
            if len(node.args) ==1:
                name = self._parse_value(node.args[0])
                self._item_rewards.append(ItemRewardDto(name, 1))
            elif len(node.args) ==2:
                name = self._parse_value(node.args[0])
                count =  self._parse_value(node.args[1])
                self._item_rewards.append(ItemRewardDto(name, count))
            else:
                raise NotImplementedError(f"Unknown got {to_lua_source(node)}")
        elif func_name == "got_money":
            self._money_rewards.append([self._parse_value(arg) for arg in node.args])
        elif func_name == "create":
            if len(node.args) == 4:
                name= self._parse_value(node.args[0])
                xyz = node.args[1]
                xyz_raw = to_lua_source(xyz)
                x = None
                y = None
                z = None
                level_vertex = self._parse_value(node.args[2])
                game_vertex_id = self._parse_value(node.args[3])
                self._spawn_rewards.append(SpawnDto(name, x, y, z, level_vertex, game_vertex_id, to_lua_source(node),xyz_raw))
            elif len(node.args) == 5:
                name= self._parse_value(node.args[0])
                xyz = node.args[1]
                xyz_raw = to_lua_source(xyz)
                x = None
                y = None
                z = None
                if isinstance(xyz, Call) and len(xyz.args) == 3:
                    x = self._parse_value(xyz.args[0])
                    y = self._parse_value(xyz.args[1])
                    z = self._parse_value(xyz.args[2])
                level_vertex = self._parse_value(node.args[2])
                game_vertex_id = self._parse_value(node.args[3])
                target_id = self._parse_value(node.args[4])
                self._spawn_rewards.append(SpawnDto(name, x, y, z, level_vertex, game_vertex_id, to_lua_source(node),xyz_raw,target_id))
            elif len(node.args) == 1:
                return
            else:
                raise NotImplementedError(f"Unknown create {to_lua_source(node)}")
        else:
            self._nested_calls.append(to_lua_source(node.func))

    def _parse_value(self, arg):
        if isinstance(arg, Number):
            return arg.n
        if isinstance(arg, String):
            return arg.s
        if isinstance(arg, Index):
            return f"<variable>{to_lua_source(arg)}"
        if isinstance(arg, Nil):
            return "nil"
        if isinstance(arg, Name):
            return f"<variable>{to_lua_source(arg)}"
        if isinstance(arg, Op):
            return f"<op>{to_lua_source(arg)}"
        if isinstance(arg, Call):
            return f"<call>{to_lua_source(arg)}"
        if isinstance(arg, UnaryOp):
            return f"{to_lua_source(arg)}"
        if isinstance(arg, Invoke):
            return f"<invoke>{to_lua_source(arg)}"
        raise NotImplementedError(f"{arg.__class__} is not implemented")

    def get_results(self) -> dict:
        return {
            "items": self._item_rewards,
            "money": self._money_rewards,
            "spawn": self._spawn_rewards,
            "nested": self._nested_calls,
        }


class FunctionsVisitor(ASTVisitor):
    def __init__(self):
        super().__init__()
        self._function_rewards = {}

    @log_parse_error
    def visit_Function(self, node: Function) -> None:
        current_function_name = to_lua_source(node.name)
        nested_visitor = NestedCallsVisitor()
        nested_visitor.visit(node)
        self._function_rewards[current_function_name] = nested_visitor.get_results()

    def rewards(self) -> dict:
        return self._function_rewards

class Command(BaseCommand):

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "scripts"

    def get_files_paths(self, path: Path) -> list[Path]:
        paths = []
        for (dir, _, files) in os.walk(path):
            for file_name in files:
                paths.append(Path(os.path.join(dir, file_name)))

        return paths

    def _get_namespace(self, file_path: Path) -> str:
        path = file_path.relative_to(self.get_files_dir_path())
        path = str(path)
        path = path[:-len(".script")]
        return path.replace("\\", ".")

    @atomic
    def handle(self, **options) -> None:
        MoneyReward.objects.all().delete()
        ItemReward.objects.all().delete()
        SpawnReward.objects.all().delete()
        ScriptFunction.objects.all().delete()

        script_files = self.get_files_paths(self.get_files_dir_path())
        exclude_files = {self.get_files_dir_path()/"lua_help.script"}

        functions_by_aliases: dict[str, ScriptFunction] = {}

        for script_file in script_files:
            print(f"START {script_file}")
            if script_file in exclude_files:
                continue
            file_namespace = self._get_namespace(script_file)
            print(f"{file_namespace=}")
            with open(script_file) as file:
                src = file.read()

            tree = parse(src)
            visitor = FunctionsVisitor()
            visitor.visit(tree)
            rewards = visitor.rewards()
            for function_name, reward in rewards.items():
                func = ScriptFunction.objects.create(name=function_name, namespace=file_namespace)
                function_aliases = self._create_function_aliases(function_name, file_namespace)
                for alias in function_aliases:
                    if alias in functions_by_aliases:
                        logger.warning(f"Для {alias} несколько функций {functions_by_aliases[alias]}, {func} ")
                    functions_by_aliases[alias] = func

                func.raw_nested_function = ";".join(reward["nested"])
                func.save()

                for money in reward["money"]:
                    raw_value = money[0]
                    value = None
                    try:
                        value = decimal.Decimal(raw_value)
                    except (TypeError, ValueError, decimal.InvalidOperation):
                        logger.warning(f"Decimal parsing error {raw_value=}")

                    MoneyReward.objects.create(function=func, raw_count=raw_value, count=value)

                for item in reward["items"]:
                    item_name = item.item_name
                    items_count_str = item.count
                    items_count = None
                    try:
                        items_count = int(items_count_str)
                    except (TypeError, ValueError, decimal.InvalidOperation):
                        logger.warning(f"int parsing error {items_count_str=}")

                    ItemReward.objects.create(function=func, raw_count=items_count_str, raw_item=item_name, count=items_count)

                for item in reward["spawn"]:
                    level_vertex = None
                    try:
                        level_vertex = int(item.level_vertex)
                    except (TypeError, ValueError, decimal.InvalidOperation):
                        logger.warning(f"int parsing error {item.level_vertex=}")

                    game_vertex_id = None
                    try:
                        game_vertex_id = int(item.game_vertex_id)
                    except (TypeError, ValueError, decimal.InvalidOperation):
                        logger.warning(f"int parsing error {item.game_vertex_id=}")

                    SpawnReward.objects.create(
                        function=func,
                        x=item.x,
                        y=item.y,
                        z=item.z,
                        raw_maybe_item=item.item_or_npc_name,
                        raw_level_vertex=item.level_vertex,
                        raw_game_vertex_id=item.game_vertex_id,
                        raw_call=item.raw,
                        xyz_raw=item.xyz_raw,
                        level_vertex=level_vertex,
                        game_vertex_id=game_vertex_id,
                        raw_target=item.target,
                    )

        for func in ScriptFunction.objects.all():
            nested_func_names = func.raw_nested_function.split(";")
            nested_functions = [functions_by_aliases.get(func_name, None) for func_name in nested_func_names]
            nested_functions = [f for f in nested_functions if f is not None]
            if len(nested_func_names) != len(nested_functions):
                founded = {str(f) for f in nested_functions}
                not_found = set(nested_func_names) - founded
                logger.warning(f"Set nested functions {not_found=}")
            func.nested_function.set(nested_functions)

    def _create_function_aliases(self, function_name, file_namespace) -> list[str]:
        name = function_name
        names = [name]
        namespace_parts = list(reversed(file_namespace.split(".")))
        for part in namespace_parts:
            name=f"{part}.{name}"
            names.append(name)
        return names
