from django.db import models

from game_parser.models import Translation


class Dialog(models.Model):
    class Meta:
        verbose_name = 'Диалог'

    game_id = models.CharField(max_length=512, null=False, verbose_name='id')
    has_info_raw = models.TextField(null=True)
    dont_has_info_raw = models.TextField(null=True)
    give_info_raw = models.TextField(null=True)
    actions_raw = models.TextField(null=True)
    precondition_raw = models.TextField(null=True)
    init_func_raw = models.TextField(null=True)
    comments_raw = models.TextField(null=True)


class DialogPhrase(models.Model):
    local_id = models.CharField(max_length=10)

    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=False)

    text_id_raw = models.CharField(max_length=256, null=True)
    text = models.ForeignKey(Translation, null=True, on_delete=models.SET_NULL)

    next_ids_raw = models.CharField(max_length=512)
    previous = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    give_info_raw = models.TextField(null=True)
    actions_raw = models.TextField(null=True)
    precondition_raw = models.TextField(null=True)
    has_info_raw = models.TextField(null=True)
    dont_has_info_raw = models.TextField(null=True)
    disable_info_raw = models.TextField(null=True)
    disable_raw = models.TextField(null=True)
