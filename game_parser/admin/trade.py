from django.contrib.admin import ModelAdmin, register

from game_parser.models import Trader, Buy, Sell, ItemInBuy, ItemInSell


@register(Trader)
class TraderAdmin(ModelAdmin):
    pass


@register(Buy)
class BuyAdmin(ModelAdmin):
    pass


@register(Sell)
class SellAdmin(ModelAdmin):
    pass


@register(ItemInBuy)
class ItemInBuyAdmin(ModelAdmin):
    pass


@register(ItemInSell)
class ItemInSellAdmin(ModelAdmin):
    pass
