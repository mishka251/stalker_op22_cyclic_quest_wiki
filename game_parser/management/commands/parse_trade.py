import logging
import re
from decimal import Decimal
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.logic.ltx_parser import LtxParser
from game_parser.models import Buy, ItemInBuy, ItemInSell, Sell, Trader

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_files_dir_path(self) -> Path:
        base_path = settings.OP22_GAME_DATA_PATH
        return base_path / "config" / "trade"

    _excluded_files = {
        "generic.ltx",
        "tm_brother.ltx",
    }

    def get_files_paths(self) -> list[Path]:
        paths = []
        for file_name in self.get_files_dir_path().iterdir():
            if file_name.name in self._excluded_files:
                continue
            paths.append(file_name)
        return paths

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        # pylint: disable=too-many-locals
        Trader.objects.all().delete()
        Buy.objects.all().delete()
        Sell.objects.all().delete()
        ItemInBuy.objects.all().delete()
        ItemInSell.objects.all().delete()

        for file in self.get_files_paths():
            print(f"start {file}")
            parser = LtxParser(file)
            results = parser.get_parsed_blocks()
            trader_name = file.name[:-4]
            trader = Trader.objects.create(
                game_code=trader_name,
                source_file=file.name,
            )

            main_block_name = "trader"
            main_block = results.pop(main_block_name)
            if not isinstance(main_block, dict):
                raise TypeError
            buy_section_name = main_block.pop("buy_condition")
            print("\tbuy")
            buy_section_raw = results.pop(buy_section_name)
            if not isinstance(buy_section_raw, dict):
                raise TypeError
            if buy_section_raw is None:
                raise TypeError
            buy_section = self._clean_section(buy_section_raw)
            self._create_buy(trader, buy_section_name, buy_section)

            sell_str = main_block.pop("sell_condition")
            supplies_str = main_block.pop("buy_supplies")

            sells = [s.strip() for s in sell_str.split(",")]
            supplies = [s.strip() for s in supplies_str.split(",")]
            for sell, supply in zip(sells, supplies, strict=True):
                sell_condition, sell_section_name = self._parse_condition(sell)
                supply_condition, supply_section_name = self._parse_condition(supply)

                if sell_condition != supply_condition:
                    msg = f"{sell_condition=}, {supply_condition=}"
                    raise ValueError(msg)
                print(f"\t{sell_section_name=}, {supply_section_name=}")
                supply_section_raw = results.pop(supply_section_name)
                if not isinstance(supply_section_raw, dict):
                    raise TypeError
                supply_section = self._clean_section(supply_section_raw)
                sell_section_raw = results.pop(sell_section_name)
                if not isinstance(sell_section_raw, dict):
                    raise TypeError
                sell_section = self._clean_section(sell_section_raw)
                self._create_sell(
                    trader,
                    sell_section_name,
                    supply_section,
                    sell_section,
                    sell_condition,
                )
            print(f"end {file}")

    def _parse_condition(self, trade_with_condition_str: str) -> tuple[str | None, str]:
        condition_patter = re.compile(r"\{(?P<condition>.*)} (?P<section_name>\w*)")
        match = condition_patter.match(trade_with_condition_str)
        if match:
            condition = match.groupdict()["condition"]
            section_name = match.groupdict()["section_name"]
            return condition, section_name
        return None, trade_with_condition_str

    def _create_buy(
        self,
        trader: Trader,
        section_name: str,
        data: dict[str, str],
    ) -> None:
        buy = Buy.objects.create(trader=trader, name=section_name)
        for item_name, item_str in data.items():
            try:
                min_price_str, max_price_str = item_str.split(",")
            except Exception as e:
                msg = f"Кривая строка {item_name} {item_str}"
                raise ValueError(msg) from e
            min_price = Decimal(min_price_str.strip())
            max_price = Decimal(max_price_str.strip())
            ItemInBuy.objects.create(
                min_price_modifier=min_price,
                max_price_modifier=max_price,
                trade=buy,
                item_name=item_name,
            )

    # pylint: disable=too-many-arguments
    def _create_sell(
        self,
        trader: Trader,
        section_name: str,
        supply_data: dict[str, str],
        price_section: dict[str, str],
        condition: str | None,
    ) -> None:
        # pylint: disable=too-many-locals
        sell = Sell.objects.create(
            trader=trader,
            name=section_name,
            condition=condition,
        )
        possible_keys = set(supply_data.keys()) & set(price_section.keys())
        for item_name in possible_keys:
            try:
                item_str = supply_data.pop(item_name)
                price_str = price_section.pop(item_name)
                min_price_str, max_price_str = price_str.split(",")
                min_price = Decimal(min_price_str.strip())
                max_price = Decimal(max_price_str.strip())
                count_str, probability_str = item_str.split(",")
                probability = Decimal(probability_str.strip())
                count = int(count_str.strip())
                ItemInSell.objects.create(
                    min_price_modifier=min_price,
                    max_price_modifier=max_price,
                    probability=probability,
                    count=count,
                    trade=sell,
                    item_name=item_name,
                )
            except Exception as ex:
                print(f"{item_name=}, {ex=}")
                raise

        if price_section:
            logger.warning(
                f"Not in supply, but in prices {price_section}, {trader.game_code}, {section_name=}",
            )
        if supply_data:
            logger.warning(
                f"Not in prices, but in supply {supply_data}, {trader.game_code}, {section_name=}",
            )

    def _clean_section(self, section: dict[str, str]) -> dict[str, str]:
        return {key: value for key, value in section.items() if value is not None}
