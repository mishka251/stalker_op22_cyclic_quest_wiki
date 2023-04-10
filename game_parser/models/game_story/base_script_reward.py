from django.db import models

from .script_function import ScriptFunction
from polymorphic.models import PolymorphicModel


class BaseScriptReward(PolymorphicModel):
    class Meta:
        ...

    function = models.ForeignKey(ScriptFunction, related_name='rewards', on_delete=models.SET_NULL, null=True)
