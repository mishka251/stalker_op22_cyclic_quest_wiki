import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import Icon, Monster, MonsterPart, Translation

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options) -> None:
        count = Monster.objects.count()
        for index, item in enumerate(Monster.objects.all()):
            if item.short_name:
                item.name_translation = Translation.objects.filter(
                    code=item.short_name
                ).first()
            if item.icon_str:
                item.icon = Icon.objects.filter(name=item.icon_str).first()
            if item.Spawn_Inventory_Item_Section:
                item.monster_part = (
                    MonsterPart.objects.filter(
                        name=item.Spawn_Inventory_Item_Section
                    ).first()
                    or MonsterPart.objects.filter(
                        inv_name=item.Spawn_Inventory_Item_Section
                    ).first()
                )
            item.save()
            print(f"{index+1}/{count}")
