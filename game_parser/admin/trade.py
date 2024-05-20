from decimal import Decimal

from django.contrib.admin import ModelAdmin, display, register
from django.utils.safestring import mark_safe

from game_parser.admin.utils import SpawnItemMapRenderer, SpawnRewardMapRenderer
from game_parser.models import (
    Buy,
    CustomSpawnItem,
    ItemInBuy,
    ItemInSell,
    NpcLogicConfig,
    Sell,
    SpawnItem,
    Trader,
)
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

    list_display = [
        "__str__",
        "map",
    ]

    @display(description="Карта")
    def map(self, obj: Trader) -> str | None:
        rendered_maps = []
        for npc_config in obj.npclogicconfig_set.all():
            if not isinstance(npc_config, NpcLogicConfig):
                raise TypeError
            rendered_maps += self._collect_npc_config_maps(npc_config)
        if rendered_maps:
            return mark_safe("\n\n".join(rendered_maps))
        return None

    def _collect_npc_config_maps(self, npc_config: NpcLogicConfig) -> list[str]:
        rendered_maps = []
        for spawn_item in npc_config.spawnitem_set.all():
            if not isinstance(spawn_item, SpawnItem):
                raise TypeError
            renderer = SpawnItemMapRenderer(spawn_item)
            rendered_map = renderer.render()
            if rendered_map:
                rendered_maps.append(rendered_map)
        for custom_spawn_item in npc_config.customspawnitem_set.all():
            if not isinstance(custom_spawn_item, CustomSpawnItem):
                raise TypeError
            for spawn_reward in custom_spawn_item.spawn_rewards.all():
                maybe_rendered_map = SpawnRewardMapRenderer(spawn_reward).render()
                if maybe_rendered_map:
                    rendered_maps.append(maybe_rendered_map)
        return rendered_maps


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
