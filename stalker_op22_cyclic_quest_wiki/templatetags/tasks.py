from typing import Any

from django.template import Library
from django.template.loader import render_to_string

from stalker_op22_cyclic_quest_wiki.services.tasks.tasks_grouping import (
    AmmoTarget,
    CharacterQuests,
    LagerTarget,
    QuestItemTarget,
    QuestItemWithStateTarget,
    StalkerTarget,
    TaskAmmoReward,
    TaskItemReward,
    TaskMoneyReward,
    TaskRandomReward,
    TaskReward,
    TreasureReward,
)

register = Library()


@register.simple_tag
def render_task(task: CharacterQuests) -> str:
    template_name = "wiki/vendor_quests_list/task.html"
    context = {"task": task}
    return render_to_string(template_name, context)


@register.simple_tag
def render_reward(reward: TaskReward) -> str:
    template_name = None
    if isinstance(reward, TaskMoneyReward):
        template_name = "wiki/vendor_quests_list/reward/money_reward.html"
    elif isinstance(reward, TaskAmmoReward):
        template_name = "wiki/vendor_quests_list/reward/ammo_reward.html"
    elif isinstance(reward, TaskItemReward):
        template_name = "wiki/vendor_quests_list/reward/item_reward.html"
    elif isinstance(reward, TreasureReward):
        template_name = "wiki/vendor_quests_list/reward/treasure_reward.html"
    elif isinstance(reward, TaskRandomReward):
        template_name = "wiki/vendor_quests_list/reward/random_reward.html"
    else:
        msg = f"{reward.__class__}"
        raise NotImplementedError(msg)
    context = {
        "reward": reward,
    }
    return render_to_string(template_name, context)


@register.simple_tag
def render_target(target: TaskReward) -> str:
    template_name = None
    context: dict[str, Any] = {
        "target": target,
    }
    if isinstance(target, AmmoTarget):
        template_name = "wiki/vendor_quests_list/target/ammo_target.html"
    elif isinstance(target, QuestItemWithStateTarget):
        template_name = "wiki/vendor_quests_list/target/item_with_state_target.html"
    elif isinstance(target, QuestItemTarget):
        template_name = "wiki/vendor_quests_list/target/item_target.html"
    elif isinstance(target, LagerTarget):
        template_name = "wiki/vendor_quests_list/target/lager_target.html"
    elif isinstance(target, StalkerTarget):
        template_name = "wiki/vendor_quests_list/target/stalker_target.html"
    else:
        msg = f"{target.__class__}"
        raise NotImplementedError(msg)

    return render_to_string(template_name, context)
