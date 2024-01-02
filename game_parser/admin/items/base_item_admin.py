from decimal import Decimal
from typing import Optional

from django.contrib.admin import ModelAdmin, register, display, TabularInline
from django.utils.safestring import mark_safe

from game_parser.models import ItemReward, SpawnReward, CyclicQuest, ItemInSell, ItemInBuy, QuestRandomReward, \
    ItemInTreasure
from game_parser.models.items.base_item import BaseItem
from game_parser.models.quest import CyclicQuestItemReward
from game_parser.utils.admin_utils.icon_view import icon_view
from game_parser.utils.admin_utils.readonly_nested_table import ReadOnlyNestedTable


class ItemQuestRewardInlineAdmin(ReadOnlyNestedTable):
    model = ItemReward
    verbose_name = 'Функция с выдачей предмета'
    verbose_name_plural = 'Функции с выдачей предмета'

    exclude = (
        'raw_item',
        'raw_count',
    )


class ItemQuestSpawnRewardInlineAdmin(ReadOnlyNestedTable):
    model = SpawnReward
    verbose_name = 'Функция со спавном предмета'
    verbose_name_plural = 'Функции со спавном предмета'
    exclude = (
        'raw_maybe_item',
        'x',
        'y',
        'z',
        'raw_level_vertex',
        'raw_game_vertex_id',
        'level_vertex',
        'game_vertex_id',
        'xyz_raw',
        'raw_target',
    )


class CyclicQuestRewardInline(ReadOnlyNestedTable):
    model = CyclicQuestItemReward
    verbose_name = 'Цикличка, где получаем как награду'
    verbose_name_plural = 'Циклички, где получаем как награду'


class CyclicQuestTargetInline(ReadOnlyNestedTable):
    model = CyclicQuest
    verbose_name = 'Цикличка, где требуется'
    verbose_name_plural = 'Циклички, где требуется'


class TradingWhereSell(ReadOnlyNestedTable):
    model = ItemInSell
    verbose_name = 'Можно купить'
    verbose_name_plural = 'Можно купить'

    readonly_fields = [
        "price_from",
        "price_to",
    ]

    ordering = [
        "min_price_modifier",
        "max_price_modifier",
    ]

    @display(description="Цена(ОТ)", ordering="min_price_modifier")
    def price_from(self, trade: ItemInSell) -> Decimal:
        return trade.item.cost*trade.min_price_modifier

    @display(description="Цена(ДО)", ordering="max_price_modifier")
    def price_to(self, trade: ItemInSell) -> Decimal:
        return trade.item.cost*trade.max_price_modifier


class TradingWhereBuy(ReadOnlyNestedTable):
    model = ItemInBuy
    verbose_name = 'Можно продать'
    verbose_name_plural = 'Можно продать'

    readonly_fields = [
        "price_from",
        "price_to",
    ]

    ordering = [
        "-min_price_modifier",
        "-max_price_modifier",
    ]

    @display(description="Цена(ОТ)", ordering="min_price_modifier")
    def price_from(self, trade: ItemInBuy) -> Decimal:
        return trade.item.cost*trade.min_price_modifier

    @display(description="Цена(ДО)", ordering="max_price_modifier")
    def price_to(self, trade: ItemInBuy) -> Decimal:
        return trade.item.cost*trade.max_price_modifier


class RandomReward(ReadOnlyNestedTable):
    model = QuestRandomReward.possible_items.through
    verbose_name = 'Случайная награда'
    verbose_name_plural = 'В случайных наградах'


class TreasureItemsAdmin(ReadOnlyNestedTable):
    model = ItemInTreasure


@register(BaseItem)
class BaseItemAdmin(ModelAdmin):
    list_display = (
        'name_translation_rus',
        'description_translation_rus',
        'inv_icon_view',
    )

    search_fields = [
        'inv_name',
        'name',
    ]

    inlines = [
        ItemQuestRewardInlineAdmin,
        ItemQuestSpawnRewardInlineAdmin,
        CyclicQuestRewardInline,
        CyclicQuestTargetInline,
        TradingWhereSell,
        TradingWhereBuy,
        RandomReward,
        TreasureItemsAdmin,
    ]

    autocomplete_fields = [
        'name_translation',
        'description_translation',
    ]

    @display(description='Название', ordering='name_translation__rus')
    def name_translation_rus(self, obj: BaseItem) -> str:
        if obj.name_translation:
            return obj.name_translation.rus
        return obj.inv_name

    @display(description='Описание')
    def description_translation_rus(self, obj: BaseItem) -> str:
        if obj.description_translation:
            return obj.description_translation.rus
        return obj.description_code

    @display(description='Иконка', )
    def inv_icon_view(self, obj: BaseItem) -> Optional[str]:
        return icon_view(obj.inv_icon)
