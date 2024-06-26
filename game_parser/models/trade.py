from django.db import models


class Trader(models.Model):

    game_code = models.CharField(null=False, max_length=255, unique=True)
    name = models.CharField(null=True, max_length=255)
    source_file = models.CharField(null=True, max_length=255)

    class Meta:
        verbose_name = "Профиль торговли"
        verbose_name_plural = "Профили торговли"

    def __str__(self) -> str:
        return f"Профиль торговли {self.game_code} {self.name}"


class BaseTrade(models.Model):
    trader = models.ForeignKey(
        Trader,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Торговец",
    )
    name = models.CharField(max_length=120, verbose_name="Название секции")
    condition = models.CharField(max_length=250, verbose_name="Условие", null=True)

    class Meta:
        verbose_name = "Торговля"

    def __str__(self) -> str:
        return f"{self.name} у {self.trader}"


class Buy(BaseTrade):
    class Meta:
        verbose_name = "Покупка"


class Sell(BaseTrade):
    class Meta:
        verbose_name = "Продажа"


class ItemInTradeBase(models.Model):
    item_name = models.CharField(max_length=255, verbose_name="Идентификатор предмета")
    item = models.ForeignKey(
        "BaseItem",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Предмет",
    )

    def __str__(self) -> str:
        return f"{self.item}"


class ItemInBuy(ItemInTradeBase):
    trade = models.ForeignKey(
        Buy,
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Торговля",
        related_name="items",
    )
    min_price_modifier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        verbose_name="Множитель цены(от)",
    )
    max_price_modifier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        verbose_name="Множитель цены(до)",
    )

    class Meta:
        verbose_name = "Предмет в покупке"
        verbose_name_plural = "Предметы в покупке"

    def __str__(self) -> str:
        return f"Продажа {self.item_name} в {self.trade}"


class ItemInSell(ItemInTradeBase):
    trade = models.ForeignKey(
        Sell,
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Торговля",
        related_name="items",
    )
    probability = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        verbose_name="Вероятность",
    )
    count = models.IntegerField(null=False, verbose_name="Кол-во предметов")
    min_price_modifier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        verbose_name="Множитель цены(от)",
    )
    max_price_modifier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        verbose_name="Множитель цены(до)",
    )

    class Meta:
        verbose_name = "Предмет в продаже"
        verbose_name_plural = "Предметы в продаже"

    def __str__(self) -> str:
        return f"Покупка {self.item_name} в {self.trade}"
