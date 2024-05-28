from django.template import Library
from django.template.loader import render_to_string

from stalker_op22_cyclic_quest_wiki.services.base.condition import ItemCondition

BROKEN_MAX_STATE = 50

NEW_MIN_STATE = 90

register = Library()


@register.simple_tag
def render_condition(condition: ItemCondition) -> str:
    before_width = int(condition.min)
    target_width = int(condition.max - condition.min)
    after_width = int(100 - condition.max)
    target_cond_str = None
    if condition.min >= NEW_MIN_STATE:
        target_cond_str = "Новый"
    elif condition.max <= BROKEN_MAX_STATE:
        target_cond_str = "Сломанный"

    context = {
        "before_width": before_width,
        "target_width": target_width,
        "after_width": after_width,
        "target_cond_str": target_cond_str,
        "condition": condition,
    }

    return render_to_string("wiki/widgets/condition.html", context)
