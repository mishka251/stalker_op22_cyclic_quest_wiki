from django.db import models

from game_parser.models.game_story.infoportion import InfoPortion
from game_parser.models.game_story.script_function import ScriptFunction
from game_parser.models.translation import Translation


class Dialog(models.Model):
    game_id = models.CharField(
        max_length=512,
        null=False,
        verbose_name="id",
        unique=True,
    )
    has_info_raw = models.TextField(null=True, verbose_name="id требуемых инфопоршней")
    dont_has_info_raw = models.TextField(null=True)
    give_info_raw = models.TextField(null=True)
    actions_raw = models.TextField(null=True)
    precondition_raw = models.TextField(null=True)
    init_func_raw = models.TextField(null=True)
    comments_raw = models.TextField(null=True, verbose_name="комментарии из xml")

    has_info = models.ManyToManyField(
        InfoPortion,
        related_name="open_dialogs",
        verbose_name="Информация, нужная для получения диалога",
    )
    dont_has_info = models.ManyToManyField(
        InfoPortion,
        related_name="close_dialogs",
        verbose_name="Информация, блокирующая диалог",
    )
    give_info = models.ManyToManyField(
        InfoPortion,
        related_name="activated_in_dialogs",
        verbose_name="Информация, получаемая за диалог",
    )
    precondition = models.ManyToManyField(
        ScriptFunction,
        related_name="dialogs_required_function",
        verbose_name="Функции-условия для диалога",
    )
    init_func = models.ManyToManyField(
        ScriptFunction,
        related_name="dialogs_inited",
        verbose_name="функция, инициализирующая диалог",
    )

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"

    def __str__(self):
        return f"Диалог {self.game_id}"


class DialogPhrase(models.Model):

    local_id = models.CharField(max_length=10, verbose_name="id фразы в диалоге")

    dialog = models.ForeignKey(
        Dialog,
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Диалог",
    )

    text_id_raw = models.CharField(max_length=256, null=True, verbose_name="id текста")
    text = models.ForeignKey(
        Translation,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Перевод текста",
        related_name="+",
    )

    next_ids_raw = models.CharField(
        max_length=512,
        verbose_name="id следующих фраз диалога",
    )
    previous = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Предыдущая фраза",
    )

    give_info_raw = models.TextField(null=True, verbose_name="Получение инфопоршня(id)")
    actions_raw = models.TextField(null=True, verbose_name="Запуск действий(id)")
    precondition_raw = models.TextField(null=True)
    has_info_raw = models.TextField(null=True)
    dont_has_info_raw = models.TextField(null=True)
    disable_info_raw = models.TextField(null=True)
    disable_raw = models.TextField(null=True)

    give_info = models.ManyToManyField(
        InfoPortion,
        related_name="activated_in_phrases",
        verbose_name="Информация, получаемая за фразу диалог",
    )
    actions = models.ManyToManyField(
        ScriptFunction,
        related_name="starts_phrases",
        verbose_name="Функции,запускаемые диалогом",
    )
    precondition = models.ManyToManyField(
        ScriptFunction,
        related_name="phrase_required_function",
        verbose_name="Функции-условия для фразы диалога",
    )
    has_info = models.ManyToManyField(
        InfoPortion,
        related_name="open_phrases",
        verbose_name="Информация, нужная для получения фразы диалога",
    )
    don_has_info = models.ManyToManyField(
        InfoPortion,
        related_name="close_phrases",
        verbose_name="Информация, блокирующая фразу диалог",
    )
    disable_info = models.ManyToManyField(
        InfoPortion,
        related_name="disable_info_in_phrases",
        verbose_name="Убираемые инфопоршни?",
    )
    disable = models.ManyToManyField(
        InfoPortion,
        related_name="disable_phrases",
        verbose_name="Убираемые инфопоршни?",
    )

    class Meta:
        verbose_name = "Фраза диалога"
        verbose_name_plural = "Фразы диалогов"
        constraints = [
            models.UniqueConstraint(
                fields=["local_id", "dialog"],
                name="unique_dialog_phrase_by_local_id_and_dialog",
            ),
        ]

    def __str__(self):
        return f"Фраза {self.local_id} диалога {self.dialog}"

    @property
    def get_text(self) -> str | None:
        if self.text:
            return self.text.rus
        return self.text_id_raw
