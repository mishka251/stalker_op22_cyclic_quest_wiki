import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import EncyclopediaArticle, Icon, TaskObjective, Translation

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, *args: Any, **options: Any) -> None:
        count = TaskObjective.objects.count()
        for index, item in enumerate(TaskObjective.objects.all()):
            item.text = Translation.objects.filter(code=item.text_id_raw).first()
            item.article = (
                EncyclopediaArticle.objects.filter(game_id=item.article_id_raw).first()
                or EncyclopediaArticle.objects.filter(name=item.article_id_raw).first()
            )
            item.icon = Icon.objects.filter(name=item.icon_raw).first()
            item.save()
            print(f"{index+1}/{count}")
