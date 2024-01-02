from decimal import Decimal

from django.contrib.admin import ModelAdmin, register, display

from game_parser.models import Trader, Buy, Sell, ItemInBuy, ItemInSell
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


@register(Trader)
class TraderAdmin(ModelAdmin):
    pass


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
    def price_from(self, trade: ItemInBuy) -> Decimal:
        return trade.item.cost*trade.min_price_modifier

    @display(description="Цена(ДО)", ordering="max_price_modifier")
    def price_to(self, trade: ItemInBuy) -> Decimal:
        return trade.item.cost*trade.max_price_modifier


@register(Buy)
class BuyAdmin(ModelAdmin):
    inlines = [ItemInByline]


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
    def price_from(self, trade: ItemInSell) -> Decimal:
        return trade.item.cost*trade.min_price_modifier

    @display(description="Цена(ДО)", ordering="max_price_modifier")
    def price_to(self, trade: ItemInSell) -> Decimal:
        return trade.item.cost*trade.max_price_modifier


@register(Sell)
class SellAdmin(ModelAdmin):
    inlines = [ItemInSellInline]




@register(ItemInBuy)
class ItemInBuyAdmin(ModelAdmin):
    pass


@register(ItemInSell)
class ItemInSellAdmin(ModelAdmin):
    pass
