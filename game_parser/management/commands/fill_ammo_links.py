import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Ammo, GrenadeLauncher, Scope, Silencer, Weapon

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options) -> None:
        count = Weapon.objects.count()
        partial_updated = set()

        for index, weapon in enumerate(Weapon.objects.all()):
            if weapon.scope_name:
                weapon.scope = Scope.objects.filter(name=weapon.scope_name).first()
                if not weapon.scope:
                    partial_updated.add(weapon)

            if weapon.silencer_name:
                weapon.silencer = Silencer.objects.filter(
                    name=weapon.silencer_name,
                ).first()
                if not weapon.silencer:
                    partial_updated.add(weapon)

            if weapon.grenade_launcher_name:
                weapon.grenade_launcher = GrenadeLauncher.objects.filter(
                    name=weapon.grenade_launcher_name,
                ).first()
                if not weapon.grenade_launcher:
                    partial_updated.add(weapon)
            ammo_names = [ammo.strip() for ammo in weapon.ammo_class_str.split(",")]
            ammos = Ammo.objects.filter(name__in=ammo_names)
            weapon.ammo.set(ammos)
            if len(ammo_names) != ammos.count():
                partial_updated.add(weapon)
            weapon.save()
            print(f"{index+1}/{count}")

        unfounded_items = {item.name for item in partial_updated}
        print(f"Not found = {unfounded_items}")
