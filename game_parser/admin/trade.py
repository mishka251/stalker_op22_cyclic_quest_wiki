from decimal import Decimal

from django.contrib.admin import ModelAdmin, display, register

from game_parser.models import Buy, ItemInBuy, ItemInSell, NpcLogicConfig, Sell, Trader
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class NpcLogicConfigInline(ReadOnlyNestedTable):
    model = NpcLogicConfig


@register(Trader)
class TraderAdmin(ModelAdmin):
    search_fields = [
        "game_code",
        "name",
        "source_file",
    ]

    inlines = [
        NpcLogicConfigInline,
    ]


class ItemInByline(ReadOnlyNestedTable):
    model = ItemInBuy

    readonly_fields = [
        "price_from",
        "price_to",
    ]

    ordering = [
        "item__polymorphic_ctype",
        "item__name",
    ]

    @display(description="Цена(ОТ)", ordering="min_price_modifier")
    def price_from(self, trade: ItemInBuy) -> Decimal | None:
        if (
            trade.item
            and trade.item.cost is not None
            and trade.min_price_modifier is not None
        ):
            return trade.item.cost * trade.min_price_modifier
        return None

    @display(description="Цена(ДО)", ordering="max_price_modifier")
    def price_to(self, trade: ItemInBuy) -> Decimal | None:
        if (
            trade.item
            and trade.item.cost is not None
            and trade.max_price_modifier is not None
        ):
            return trade.item.cost * trade.max_price_modifier
        return None


@register(Buy)
class BuyAdmin(ModelAdmin):
    inlines = [ItemInByline]
    autocomplete_fields = [
        "trader",
    ]

    search_fields = [
        "trader",
        "name",
    ]


class ItemInSellInline(ReadOnlyNestedTable):
    model = ItemInSell

    readonly_fields = [
        "price_from",
        "price_to",
    ]

    ordering = [
        "item__polymorphic_ctype",
        "item__name",
    ]

    @display(description="Цена(ОТ)", ordering="min_price_modifier")
    def price_from(self, trade: ItemInSell) -> Decimal | None:
        if (
            trade.item
            and trade.item.cost is not None
            and trade.min_price_modifier is not None
        ):
            return trade.item.cost * trade.min_price_modifier
        return None

    @display(description="Цена(ДО)", ordering="max_price_modifier")
    def price_to(self, trade: ItemInSell) -> Decimal | None:
        if (
            trade.item
            and trade.item.cost is not None
            and trade.max_price_modifier is not None
        ):
            return trade.item.cost * trade.max_price_modifier
        return None


@register(Sell)
class SellAdmin(ModelAdmin):
    inlines = [ItemInSellInline]
    autocomplete_fields = [
        "trader",
    ]

    search_fields = [
        "trader",
        "name",
    ]


@register(ItemInBuy)
class ItemInBuyAdmin(ModelAdmin):
    autocomplete_fields = [
        "item",
        "trade",
    ]


@register(ItemInSell)
class ItemInSellAdmin(ModelAdmin):
    autocomplete_fields = [
        "item",
        "trade",
    ]
