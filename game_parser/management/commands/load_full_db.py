from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.transaction import atomic


class Command(BaseCommand):
    another_commands = [
        # parse
        "parse_all_system",
        "parse_communities_and_ranks",
        "parse_custom_inventory_boxes",
        "parse_custom_spawn_sections",
        "parse_cycle_tasks",
        "parse_cycle_vendors",
        "parse_game_maps",
        "parse_game_story_ids",
        "parse_game_tasks",
        "parse_locations",
        "parse_npc_configs",
        "parse_recepts",
        "parse_scripts_function",
        "parse_spawn",
        "parse_spawn_camps",
        "parse_spawn_stalkers",
        "parse_stalker_sections",
        "parse_trade",
        "parse_treasures",
        # fill
        "fill_ammo_links",
        "fill_characters_dialogs",
        "fill_custom_spawn_characters_profiles",
        "fill_custom_spawn_inventory_boxes",
        "fill_cycle_tasks_random_rewards",
        "fill_cycle_tasks_vendors",
        "fill_cyclic_quest_items",
        "fill_dilog_m2m",
        "fill_dilog_phrases_translations",
        "fill_game_ids",
        "fill_game_ids_spawn_sections",
        "fill_game_stoory_ids_custom_spawn",
        "fill_game_task",
        "fill_infoportion_tasks",
        "fill_item_in_spawn",
        "fill_item_reward",
        "fill_items_icons",
        "fill_items_in_trade",
        "fill_items_translations",
        "fill_location_translations",
        "fill_monster_links",
        "fill_npc_info",
        "fill_random_reward_icons",
        "fill_random_rewards",
        "fill_random_rewards_translation",
        "fill_spawn_items_locations",
        "fill_spawn_reward",
        "fill_stalker_sections",
        "fill_storyline_character",
        "fill_task_objective",
        "fill_task_objective_links",
        "fill_task_text",
        "fill_tasks_spawn_targets",
        "fill_treasure_spawn_items",
        "fill_treasures_items",
        "fill_treasures_translations",
        "fill_vendors_for_cycle_tasks",
    ]

    @atomic
    def handle(self, *args, **options) -> None:
        for command in self.another_commands:
            print(command)
            call_command(command)
