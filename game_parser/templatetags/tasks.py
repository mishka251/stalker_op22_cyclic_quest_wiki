from game_parser.logic.tasks_grouping import CharacterQuests, TaskReward, TaskMoneyReward, TaskAmmoReward, \
    TaskItemReward, AmmoTarget, LagerTarget, StalkerTarget, QuestItemTarget
from django.template.loader import render_to_string
from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.simple_tag
def render_task(task: CharacterQuests):
    template_name = 'task.html'
    context = {"task": task}
    return render_to_string(template_name, context)


@register.simple_tag
def render_reward(reward: TaskReward):
    template_name = None
    if isinstance(reward, TaskMoneyReward):
        template_name = 'money_reward.html'
    elif isinstance(reward, TaskAmmoReward):
        template_name = 'ammo_reward.html'
    elif isinstance(reward, TaskItemReward):
        template_name = 'item_reward.html'
    else:
        raise NotImplementedError(f'{reward.__class__}')
    context = {
        'reward': reward
    }
    return render_to_string(template_name, context)


@register.simple_tag
def render_target(target: TaskReward):
    template_name = None
    if isinstance(target, AmmoTarget):
        template_name = 'ammo_target.html'
    elif isinstance(target, QuestItemTarget):
        template_name = 'item_target.html'
    elif isinstance(target, LagerTarget):
        template_name = 'lager_target.html'
    elif isinstance(target, StalkerTarget):
        template_name = 'stalker_target.html'
    else:
        raise NotImplementedError(f'{target.__class__}')
    context = {
        'target': target
    }
    return render_to_string(template_name, context)