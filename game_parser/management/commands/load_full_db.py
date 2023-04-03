from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.transaction import atomic


class Command(BaseCommand):
    another_commands = [
        # parse
        'parse_artefacts',
        'parse_cycle_tasks',
        'parse_dialogs',
        'parse_game_icons',
        'parse_game_tasks',
        'parse_icon',
        'parse_infoportions',
        'parse_locations',
        'parse_mutant_parts',
        'parse_other',
        'parse_outfit',
        'parse_scripts_function',
        'parse_storyline_character',
        'parse_trade',
        'parse_translations',
        'parse_treasures',
        'parse_weapon',

        # fill
        'fill_cyclic_quest_items',
        'fill_items_in_trade',
        'fill_items_translations',
        'fill_location_translations',
        'fill_treasures_items',
        'fill_treasures_translations',
    ]

    @atomic
    def handle(self, **options):
        for command in self.another_commands:
            print(command)
            call_command(command)
