from django.db import models


class CommunityManager(models.Manager["Community"]):
    def get_by_natural_key(self, name: str) -> "Community":
        return self.get(name=name)


class Community(models.Model):

    name = models.CharField(max_length=128, null=False, unique=True, verbose_name="Код")
    translation = models.ForeignKey(
        "Translation",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Название",
        related_name="+",
    )

    objects = CommunityManager()

    class Meta:
        verbose_name = "Группировка"
        verbose_name_plural = "Группировки"

    def __str__(self) -> str:
        return self.translation.rus

    def natural_key(self) -> tuple:
        return (self.name,)


class StalkerRankManager(models.Manager["StalkerRank"]):
    def get_by_natural_key(self, name: str) -> "StalkerRank":
        return self.get(name=name)


class StalkerRank(models.Model):

    name = models.CharField(max_length=128, null=False, unique=True, verbose_name="Код")
    translation = models.ForeignKey(
        "Translation",
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Название",
        related_name="+",
    )

    objects = StalkerRankManager()

    class Meta:
        verbose_name = "Ранг сталкера"
        verbose_name_plural = "Ранги сталкеров"

    def __str__(self) -> str:
        return self.translation.rus

    def natural_key(self) -> tuple:
        return (self.name,)


__all__ = [
    "Community",
    "StalkerRank",
]
