import logging
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from luaparser import ast, astnodes
from luaparser.ast import parse, to_lua_source
from lupa import LuaRuntime

from game_parser.models import BaseItem, InfoPortion
from game_parser.models.recepti import Recept

lua = LuaRuntime(unpack_returned_tuples=True)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "scripts" / "amk" / "amk_mod.script"

    @atomic
    def handle(self, **options) -> None:
        Recept.objects.all().delete()
        file_path = self.get_files_dir_path()
        with file_path.open("r") as file:
            parsed = parse(file.read())
        receipt: astnodes.Table | None = None
        for node in ast.walk(parsed):
            if not isinstance(node, astnodes.Assign):
                continue
            if len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, astnodes.Name):
                continue
            if target.id != "anom_recept_komp":
                continue
            receipt = node.values[0]  # noqa: PD011

        lua.execute("function translate(s) return s end")
        t = lua.eval(to_lua_source(receipt))

        global_defaults = t["default"]
        for anom_id, anom_receipts_ in t["anomalii"].items():
            anom_default_name = anom_receipts_["name"]
            anom_defaults = anom_receipts_["default"]
            anom_receipts = anom_receipts_["recepti"]
            for receipt_condition, receipt in anom_receipts.items():
                print(anom_id, receipt_condition, receipt)
                komponents = self._get_value(
                    receipt,
                    anom_defaults,
                    global_defaults,
                    "komp",
                )
                cel = self._get_value(receipt, anom_defaults, global_defaults, "cel")
                vremya = self._get_value(
                    receipt,
                    anom_defaults,
                    global_defaults,
                    "vremya",
                )
                v_udachi = self._get_value(
                    receipt,
                    anom_defaults,
                    global_defaults,
                    "v_udachi",
                )
                v_virogd = self._get_value(
                    receipt,
                    anom_defaults,
                    global_defaults,
                    "v_virogd",
                )
                remove_anomaly = self._get_value(
                    receipt,
                    anom_defaults,
                    global_defaults,
                    "remove_anomaly",
                )
                not_for_mutator = self._get_value(
                    receipt,
                    anom_defaults,
                    global_defaults,
                    "not_for_mutator",
                )
                info = self._get_value(receipt, anom_defaults, global_defaults, "info")

                komponents = list(komponents.keys())
                cel = list(cel.keys())
                if len(cel) == 1:
                    cel = cel[0]
                else:
                    raise ValueError(f"unknown {cel=}")
                (vremya_day, vremya_hour, vremya_min) = vremya[1], vremya[2], vremya[3]

                recept = Recept.objects.create(
                    anomaly_id=anom_id,
                    anomaly_name=anom_default_name,
                    condition_raw=receipt_condition,
                    condition=InfoPortion.objects.filter(
                        game_id=receipt_condition,
                    ).first(),
                    components_raw="".join(komponents),
                    cel_raw=cel,
                    cel=(
                        BaseItem.objects.filter(name=cel).first()
                        or BaseItem.objects.filter(inv_name=cel).first()
                    ),
                    v_udachi=v_udachi,
                    v_virogd=v_virogd,
                    v_ottorg=1 - v_udachi - v_virogd,
                    vremya_day=vremya_day,
                    vremya_hour=vremya_hour,
                    vremya_min=vremya_min,
                    remove_anomaly=remove_anomaly or False,
                    not_for_mutator=not_for_mutator or False,
                    info_raw=info,
                    info=InfoPortion.objects.filter(game_id=info).first(),
                )
                components = []
                for comp in komponents:
                    component = (
                        BaseItem.objects.filter(name=comp).first()
                        or BaseItem.objects.filter(inv_name=comp).first()
                    )
                    if component is None:
                        raise ValueError(f"{comp=} не найден")
                    components.append(
                        component,
                    )
                recept.components.set(components)

    def _get_value(self, recept, anom_defaults, global_defaults, attr_name):
        value = recept[attr_name]
        if value is None:
            value = anom_defaults[attr_name]
        if value is None:
            value = global_defaults[attr_name]
        return value
