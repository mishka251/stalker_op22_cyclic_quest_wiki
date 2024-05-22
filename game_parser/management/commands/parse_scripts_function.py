import dataclasses
import decimal
import logging
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from luaparser.ast import (
    ASTVisitor,
    Call,
    Function,
    Index,
    Invoke,
    Name,
    Nil,
    Number,
    Op,
    String,
    UnaryOp,
    parse,
    to_lua_source,
)

from game_parser.models import ItemReward, MoneyReward, ScriptFunction, SpawnReward

logger = logging.getLogger(__name__)


def log_parse_error(func: Callable[[Any, Any], None]) -> Callable[[Any, Any], None]:
    def wrapper(self: Any, node: Any) -> None:
        try:
            func(self, node)
        except Exception:
            logger.exception("Ошибка при парсинге %s", to_lua_source(node))
            raise

    return wrapper


@dataclasses.dataclass
class ItemRewardDto:
    item_name: str
    count: int | None = None
    count_raw: str | None = None


@dataclasses.dataclass
class SpawnDto:
    # pylint: disable=too-many-instance-attributes
    item_or_npc_name: str
    x: float | None
    y: float | None
    z: float | None
    level_vertex_raw: str
    level_vertex: int | None
    game_vertex_id_raw: str
    game_vertex_id: int | None
    raw: str
    xyz_raw: str
    target: str | None = None


@dataclasses.dataclass
class NestedCallsResultDto:
    items: list[ItemRewardDto]
    money: list[list[str]]
    nested: list[str]
    spawn: list[SpawnDto]


class NestedCallsVisitor(ASTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self._money_rewards: list[list[str]] = []
        self._item_rewards: list[ItemRewardDto] = []
        self._nested_calls: list[str] = []
        self._spawn_rewards: list[SpawnDto] = []

    @log_parse_error
    def visit_Call(self, node: Call) -> None:  # noqa: N802
        # pylint: disable=too-many-branches
        node_func = node.func

        if isinstance(node.func, Call):
            return

        func_name = (
            to_lua_source(node_func) if isinstance(node_func, Index) else node_func.id
        )

        if func_name == "got":
            if len(node.args) == 1:
                name = self._parse_value(node.args[0])
                self._item_rewards.append(ItemRewardDto(name, 1, count_raw="1"))
            elif len(node.args) == 2:  # noqa: PLR2004
                name = self._parse_value(node.args[0])
                count_raw = self._parse_value(node.args[1])
                try:
                    count = int(count_raw)
                except ValueError:
                    count = None
                self._item_rewards.append(
                    ItemRewardDto(name, count=count, count_raw=count_raw),
                )
            else:
                msg = f"Unknown got {to_lua_source(node)}"
                raise NotImplementedError(msg)
        elif func_name == "got_money":
            self._money_rewards.append([self._parse_value(arg) for arg in node.args])
        elif func_name == "create":
            self._handle_create(node)

        elif func_name in {"spawn_item", "amk.spawn_item"}:
            self._handle_amk_spawn(node)
        else:
            self._nested_calls.append(to_lua_source(node.func))

    def _handle_amk_spawn(self, node: Call) -> None:
        self._handle_create(node)

    def _handle_create(self, node: Call) -> None:
        if len(node.args) == 4:  # noqa: PLR2004
            name = self._parse_value(node.args[0])
            xyz = node.args[1]
            xyz_raw = to_lua_source(xyz)
            x = None
            y = None
            z = None
            level_vertex_raw = self._parse_value(node.args[2])
            game_vertex_id_raw = self._parse_value(node.args[3])
            level_vertex = self._try_parse_int(level_vertex_raw)
            game_vertex_id = self._try_parse_int(game_vertex_id_raw)
            self._spawn_rewards.append(
                SpawnDto(
                    name,
                    x,
                    y,
                    z,
                    level_vertex_raw=level_vertex_raw,
                    level_vertex=level_vertex,
                    game_vertex_id_raw=game_vertex_id_raw,
                    game_vertex_id=game_vertex_id,
                    raw=to_lua_source(node),
                    xyz_raw=xyz_raw,
                ),
            )
        elif len(node.args) == 5:  # noqa: PLR2004
            name = self._parse_value(node.args[0])
            xyz = node.args[1]
            xyz_raw = to_lua_source(xyz)
            x = None
            y = None
            z = None
            if isinstance(xyz, Call) and len(xyz.args) == 3:  # noqa: PLR2004
                x = float(self._parse_value(xyz.args[0]))
                y = float(self._parse_value(xyz.args[1]))
                z = float(self._parse_value(xyz.args[2]))
            level_vertex_raw = self._parse_value(node.args[2])
            game_vertex_id_raw = self._parse_value(node.args[3])
            target_id = self._parse_value(node.args[4])
            level_vertex = self._try_parse_int(level_vertex_raw)
            game_vertex_id = self._try_parse_int(game_vertex_id_raw)
            self._spawn_rewards.append(
                SpawnDto(
                    name,
                    x,
                    y,
                    z,
                    level_vertex_raw=level_vertex_raw,
                    level_vertex=level_vertex,
                    game_vertex_id_raw=game_vertex_id_raw,
                    game_vertex_id=game_vertex_id,
                    raw=to_lua_source(node),
                    xyz_raw=xyz_raw,
                    target=target_id,
                ),
            )
        elif len(node.args) == 1:
            return
        else:
            msg = f"Unknown create {to_lua_source(node)}"
            raise NotImplementedError(msg)

    def _try_parse_int(self, maybe_int_str: str) -> int | None:
        try:
            level_vertex = int(maybe_int_str)
        except ValueError:
            level_vertex = None
        return level_vertex

    def _parse_value(self, arg: Any) -> str:  # noqa: PLR0911
        # pylint: disable=too-many-return-statements
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
        msg = f"{arg.__class__} is not implemented"
        raise NotImplementedError(msg)

    def get_results(self) -> NestedCallsResultDto:
        return NestedCallsResultDto(
            items=self._item_rewards,
            money=self._money_rewards,
            spawn=self._spawn_rewards,
            nested=self._nested_calls,
        )


class FunctionsVisitor(ASTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self._function_rewards: dict[str, NestedCallsResultDto] = {}

    @log_parse_error
    def visit_Function(self, node: Function) -> None:  # noqa: N802
        current_function_name = to_lua_source(node.name)
        nested_visitor = NestedCallsVisitor()
        nested_visitor.visit(node)
        self._function_rewards[current_function_name] = nested_visitor.get_results()

    def rewards(self) -> dict[str, NestedCallsResultDto]:
        return self._function_rewards


class Command(BaseCommand):

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "scripts"

    def get_files_paths(self, path: Path) -> list[Path]:
        return [
            Path(_dir) / file_name
            for (_dir, _, files) in os.walk(path)
            for file_name in files
        ]

    def _get_namespace(self, file_path: Path) -> str:
        path = file_path.relative_to(self.get_files_dir_path())
        path_ = str(path)
        path_ = path_[: -len(".script")]
        return path_.replace("\\", ".")

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        # pylint: disable=too-many-locals, too-many-statements, too-many-branches, too-many-return-statements
        MoneyReward.objects.all().delete()
        ItemReward.objects.all().delete()
        SpawnReward.objects.all().delete()
        ScriptFunction.objects.all().delete()

        script_files = self.get_files_paths(self.get_files_dir_path())
        exclude_files = {self.get_files_dir_path() / "lua_help.script"}

        functions_by_aliases: dict[str, ScriptFunction] = {}

        for script_file in script_files:
            print(f"START {script_file}")
            if script_file in exclude_files:
                continue
            file_namespace = self._get_namespace(script_file)
            print(f"{file_namespace=}")
            with script_file.open() as file:
                src = file.read()

            tree = parse(src)
            visitor = FunctionsVisitor()
            visitor.visit(tree)
            rewards = visitor.rewards()
            for function_name, reward in rewards.items():
                func = ScriptFunction.objects.create(
                    name=function_name,
                    namespace=file_namespace,
                )
                function_aliases = self._create_function_aliases(
                    function_name,
                    file_namespace,
                )
                for alias in function_aliases:
                    if alias in functions_by_aliases:
                        logger.warning(
                            f"Для {alias} несколько функций {functions_by_aliases[alias]}, {func} ",
                        )
                    functions_by_aliases[alias] = func

                func.raw_nested_function = ";".join(reward.nested)
                func.save()

                for money in reward.money:
                    self._save_money_reward(func, money)

                for item in reward.items:
                    self._save_item_reward(func, item)

                for spawn_reward in reward.spawn:
                    self._save_spawn_reward(func, spawn_reward)
        self._save_nested_calls(functions_by_aliases)

    def _save_nested_calls(
        self,
        functions_by_aliases: dict[str, ScriptFunction],
    ) -> None:
        for func in ScriptFunction.objects.all():
            if func.raw_nested_function is None:
                raise TypeError
            nested_func_names = func.raw_nested_function.split(";")
            nested_functions_: "list[ScriptFunction | None]" = [
                functions_by_aliases.get(func_name) for func_name in nested_func_names
            ]
            nested_functions: "list[ScriptFunction]" = [
                f for f in nested_functions_ if f is not None
            ]
            if len(nested_func_names) != len(nested_functions):
                founded = {str(f) for f in nested_functions}
                not_found = set(nested_func_names) - founded
                logger.warning(f"Set nested functions {not_found=}")
            func.nested_function.set(nested_functions)

    def _save_money_reward(self, func: ScriptFunction, money: list[str]) -> None:
        raw_value = money[0]
        value = None
        try:
            value = decimal.Decimal(raw_value)
        except (TypeError, ValueError, decimal.InvalidOperation):
            logger.warning(f"Decimal parsing error {raw_value=}")
        MoneyReward.objects.create(
            function=func,
            raw_count=raw_value,
            count=value,
        )

    def _save_spawn_reward(self, func: ScriptFunction, item: SpawnDto) -> None:
        SpawnReward.objects.create(
            function=func,
            x=item.x,
            y=item.y,
            z=item.z,
            raw_maybe_item=item.item_or_npc_name,
            raw_level_vertex=item.level_vertex_raw,
            raw_game_vertex_id=item.game_vertex_id_raw,
            raw_call=item.raw,
            xyz_raw=item.xyz_raw,
            level_vertex=item.level_vertex,
            game_vertex_id=item.game_vertex_id,
            raw_target=item.target,
        )

    def _save_item_reward(self, func: ScriptFunction, item: ItemRewardDto) -> None:
        item_name = item.item_name
        ItemReward.objects.create(
            function=func,
            raw_count=item.count_raw,
            raw_item=item_name,
            count=item.count,
        )

    def _create_function_aliases(
        self,
        function_name: str,
        file_namespace: str,
    ) -> list[str]:
        name = function_name
        names = [name]
        namespace_parts = list(reversed(file_namespace.split(".")))
        for part in namespace_parts:
            name = f"{part}.{name}"
            names.append(name)
        return names
