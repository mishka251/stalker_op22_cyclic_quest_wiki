from typing import Any

from django.template import Library
from django.template.loader import render_to_string

from stalker_op22_cyclic_quest_wiki.views.cyclic_quests.tasks_grouping import CharacterQuests, TaskReward, \
    TaskMoneyReward, TaskAmmoReward, \
    TaskItemReward, AmmoTarget, LagerTarget, StalkerTarget, QuestItemTarget, QuestItemWithStateTarget, TreasureReward, \
    TaskRandomReward

register = Library()


@register.simple_tag
def render_task(task: CharacterQuests):
    template_name = 'wiki/vendor_quests_list/task.html'
    context = {"task": task}
    return render_to_string(template_name, context)


@register.simple_tag
def render_reward(reward: TaskReward):
    template_name = None
    if isinstance(reward, TaskMoneyReward):
        template_name = 'wiki/vendor_quests_list/reward/money_reward.html'
    elif isinstance(reward, TaskAmmoReward):
        template_name = 'wiki/vendor_quests_list/reward/ammo_reward.html'
    elif isinstance(reward, TaskItemReward):
        template_name = 'wiki/vendor_quests_list/reward/item_reward.html'
    elif isinstance(reward, TreasureReward):
        template_name = 'wiki/vendor_quests_list/reward/treasure_reward.html'
    elif isinstance(reward, TaskRandomReward):
        template_name = 'wiki/vendor_quests_list/reward/random_reward.html'
    else:
        raise NotImplementedError(f'{reward.__class__}')
    context = {
        'reward': reward
    }
    return render_to_string(template_name, context)


@register.simple_tag
def render_target(target: TaskReward):
    template_name = None
    context: dict[str, Any] = {
        'target': target
    }
    if isinstance(target, AmmoTarget):
        template_name = 'wiki/vendor_quests_list/target/ammo_target.html'
    elif isinstance(target, QuestItemWithStateTarget):

        context['before_width'] = int(target.state.min)
        context['target_width'] = int(target.state.max-target.state.min)
        context['after_width'] = int(100 - target.state.max)
        target_cond_str = None
        if target.state.min >= 90:
            target_cond_str = "Новый"
        elif target.state.max <= 50:
            target_cond_str = "Сломанный"
        context["target_cond_str"] = target_cond_str

        template_name = 'wiki/vendor_quests_list/target/item_with_state_target.html'
    elif isinstance(target, QuestItemTarget):
        template_name = 'wiki/vendor_quests_list/target/item_target.html'
    elif isinstance(target, LagerTarget):
        template_name = 'wiki/vendor_quests_list/target/lager_target.html'
    elif isinstance(target, StalkerTarget):
        template_name = 'wiki/vendor_quests_list/target/stalker_target.html'
    else:
        raise NotImplementedError(f'{target.__class__}')

    return render_to_string(template_name, context)
