from django.db import models

from game_parser.models.translation import Translation
from game_parser.models.game_story.storyline_character import Icon


class GameTask(models.Model):
    class Meta:
        verbose_name = "Сюжетное задание"
        verbose_name_plural = "Сюжетные задания"

    game_id = models.CharField(max_length=256, unique=True, verbose_name="Игровой id")
    title_id_raw = models.CharField(max_length=256, verbose_name="Сырое название")
    title = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL, verbose_name="Заголовок(перевод)")
    prio = models.IntegerField(null=True)

    @property
    def get_title(self) -> str:
        if self.title:
            return self.title.rus
        return self.title_id_raw

    def __str__(self):
        return self.get_title


class TaskObjective(models.Model):
    class Meta:
        verbose_name = "Цель сюжетного задания"
        verbose_name_plural = "Цели сюжетных заданий"
    task = models.ForeignKey(GameTask, on_delete=models.CASCADE, verbose_name="Задание")
    text_id_raw = models.CharField(max_length=256, null=True, verbose_name="Сырой текст")
    text = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL, related_name="+", verbose_name="Текст(перевод)")

    icon_raw = models.CharField(max_length=512, null=True, verbose_name="Название иконки")
    icon = models.ForeignKey(Icon, null=True, on_delete=models.SET_NULL, related_name="+", verbose_name="Иконка")

    article_id_raw = models.CharField(max_length=256, null=True, verbose_name="Статья(энциклопедия)")
    # article = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL, related_name='+')

    function_complete_raw = models.TextField(null=True, verbose_name="Функция, вызываемая при завершении")
    infoportion_complete_raw = models.TextField(null=True, verbose_name="Инфопоршень, устанавлеваемый при завершении")
    infoportion_set_complete_raw = models.TextField(null=True, verbose_name="Инфопоршень, устанавлеваемый при завершении")
    object_story_id_raw = models.TextField(null=True)
    function_fail_raw = models.TextField(null=True, verbose_name="Функция, вызываемая при провале")
    infoportion_set_fail_raw = models.TextField(null=True, verbose_name="Инфопоршень, устанавлеваемый при провале")
    function_call_complete_raw = models.TextField(null=True, verbose_name="Функция, вызываемая при завершении")
    # infoportion_set_fail_raw = models.TextField(null=True)

    function_complete = models.ForeignKey("ScriptFunction", related_name="on_complete_task_objective", on_delete=models.SET_NULL, null=True, verbose_name="Функция, вызываемая при завершении")
    infoportion_complete = models.ForeignKey("InfoPortion",related_name="on_complete_task_objective",  on_delete=models.SET_NULL, null=True, verbose_name="Инфопоршень, устанавлеваемый при завершении")
    infoportion_set_complete = models.ForeignKey("InfoPortion",  related_name="set_on_complete_task_objective", on_delete=models.SET_NULL, null=True, verbose_name="Инфопоршень, устанавлеваемый при завершении")
    # object_story_id_raw = models.TextField(null=True)
    function_fail = models.ForeignKey("ScriptFunction",related_name="set_on_fail_task_objective",  on_delete=models.SET_NULL, null=True, verbose_name="Функция, вызываемая при провале")
    infoportion_set_fail = models.ForeignKey("InfoPortion",  related_name="set_on_fail_task_objective", on_delete=models.SET_NULL, null=True, verbose_name="Инфопоршень, устанавлеваемый при провале")
    function_call_complete = models.ForeignKey("ScriptFunction", related_name="call_on_complete_task_objective", on_delete=models.SET_NULL, null=True, verbose_name="Функция, вызываемая при завершении")

    article = models.ForeignKey("EncyclopediaArticle", related_name="task_objectives", on_delete=models.SET_NULL, null=True, verbose_name="Статья")


    @property
    def get_text(self) -> str:
        if self.text:
            return self.text.rus
        return self.text_id_raw

    @property
    def get_article(self) -> str:
        # if self.article:
        #     return self.article.rus
        return self.article_id_raw

    def __str__(self):
        return f"{self.task} - {self.get_text}"


class MapLocationType(models.Model):
    objective = models.ForeignKey(TaskObjective, on_delete=models.CASCADE)
    hint_raw = models.CharField(max_length=256, null=True)
    hint = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL, related_name="+")
    location_type = models.CharField(max_length=256)
