from django.db import models

from .script_function import ScriptFunction
class BaseScriptReward(models.Model):
    class Meta:
        ...

    function = models.ForeignKey(ScriptFunction, related_name='rewards', on_delete=models.SET_NULL, null=True)