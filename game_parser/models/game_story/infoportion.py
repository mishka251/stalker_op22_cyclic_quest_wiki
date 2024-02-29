from django.db import models

from game_parser.models.game_story.task import GameTask


class InfoPortion(models.Model):
    class Meta:
        verbose_name = 'Инфопоршень'
        verbose_name_plural = 'Инфопоршни'

    game_id = models.CharField(max_length=512, verbose_name='Игровой идентификатор', unique=True)

    article_raw = models.CharField(max_length=256, null=True, verbose_name='Статьи(сырые id)')

    disable_raw = models.TextField(null=True, verbose_name='Отключаемые инфопоршни')

    task_raw = models.TextField(null=True, verbose_name='Задание(сырое)')
    task = models.ForeignKey(GameTask, null=True, on_delete=models.SET_NULL, verbose_name='Задание')

    actions_raw = models.TextField(null=True, verbose_name='Запускаемые функции(сырые)')
    actions = models.ManyToManyField('ScriptFunction', related_name='starts_infoportions', verbose_name='Функции,запускаемые инфопоршнем')

    def __str__(self):
        return self.game_id
