from django.db import models

from game_parser.models.game_story.dialog import Dialog


class ScriptFunction(models.Model):
    class Meta:
        verbose_name = 'Функция из скриптов'

    name = models.CharField(max_length=512, null=False, verbose_name='Название')
    namespace = models.CharField(max_length=512, null=False, verbose_name='Название файла')

    dialog = models.ForeignKey(Dialog, related_name='actions', on_delete=models.SET_NULL, null=True)
    nested_function = models.ManyToManyField('self', symmetrical=False, verbose_name='Функции, вызываемые в этой')

    raw_nested_function= models.TextField(null=True)

    def __str__(self):
        return f'{self.namespace}.{self.name}'