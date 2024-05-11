from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:

    from game_parser.models import BaseScriptReward


class ScriptFunction(models.Model):
    name = models.CharField(max_length=512, null=False, verbose_name="Название")
    namespace = models.CharField(
        max_length=512,
        null=False,
        verbose_name="Название файла",
    )

    dialog = models.ForeignKey(
        "Dialog",
        related_name="actions",
        on_delete=models.SET_NULL,
        null=True,
    )
    nested_function = models.ManyToManyField(
        "self",
        symmetrical=False,
        verbose_name="Функции, вызываемые в этой",
    )

    raw_nested_function = models.TextField(null=True)

    class Meta:
        verbose_name = "Функция из скриптов"

    rewards: "models.Manager[BaseScriptReward]"

    def __str__(self) -> str:
        return f"{self.namespace}.{self.name}"
