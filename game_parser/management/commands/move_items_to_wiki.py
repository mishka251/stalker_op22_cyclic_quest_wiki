from typing import Optional

from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from game_parser.models import Ammo as ParserAmmo
from game_parser.models import BaseItem as ParserItem
from stalker_op22_cyclic_quest_wiki.models import Ammo as WikiAmmo
from stalker_op22_cyclic_quest_wiki.models import Icon as WikiIcon
from stalker_op22_cyclic_quest_wiki.models import Item as WikiItem
from stalker_op22_cyclic_quest_wiki.models import Translation as WikiTranslation


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("START")
        self._update_ammo()
        self._update_items()
        print("END")

    def _update_ammo(self):
        print("start ammo")
        cnt = ParserAmmo.objects.count()
        for i, ammo in enumerate(ParserAmmo.objects.all()):
            icon = self._update_or_create_item_icon(ammo)
            name_translation = (
                WikiTranslation.objects.filter(code=ammo.name_translation.code).first()
                if ammo.name_translation
                else None
            )
            description_translation = (
                WikiTranslation.objects.filter(code=ammo.description_translation.code).first()
                if ammo.description_translation
                else None
            )
            if not description_translation or not name_translation or not icon:
                print(ammo)
                continue
            WikiAmmo.objects.update_or_create(
                name=ammo.name,
                defaults={
                    "box_size": ammo.box_size,
                    "cost": ammo.cost,
                    "inv_weight": ammo.inv_weight,
                    "icon": icon,
                    "name_translation": name_translation,
                    "description_translation": description_translation,
                }
            )
            if i % 100 == 0:
                print(f"{i}/{cnt}")
        print("end ammo")

    def _update_items(self):
        print("start items")
        cnt = ParserItem.objects.exclude(polymorphic_ctype=ContentType.objects.get_for_model(ParserAmmo)).count()
        for i, item in enumerate(ParserItem.objects.exclude(polymorphic_ctype=ContentType.objects.get_for_model(ParserAmmo)).all()):
            icon = self._update_or_create_item_icon(item)
            name_translation = (
                WikiTranslation.objects.filter(code=item.name_translation.code).first()
                if item.name_translation
                else None
            )
            description_translation = (
                WikiTranslation.objects.filter(code=item.description_translation.code).first()
                if item.description_translation
                else None
            )
            if not name_translation or not icon:
                print(item)
                continue
            WikiItem.objects.update_or_create(
                name=item.name,
                defaults={
                    "cost": item.cost,
                    "inv_weight": item.inv_weight,
                    "icon": icon,
                    "name_translation": name_translation,
                    "description_translation":  description_translation,
                }
            )
            if i%100==0:
                print(f"{i}/{cnt}")
        print("end items")

    def _update_or_create_item_icon(self, item: ParserItem) -> Optional[WikiIcon]:
        if not item.inv_icon:
            return None
        return WikiIcon.objects.update_or_create(
            name=f"icon_for_item_{item.name}",
            defaults={
                "icon": item.inv_icon,
            }
        )[0]