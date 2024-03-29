import logging

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from game_parser.models import TaskObjective
from game_parser.models import Translation, Icon

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @atomic
    def handle(self, **options):
        count = TaskObjective.objects.count()
        for index, item in enumerate(TaskObjective.objects.all()):
            item.text = Translation.objects.filter(code=item.text_id_raw).first()
            item.article = Translation.objects.filter(code=item.article_id_raw).first()
            item.icon = Icon.objects.filter(name=item.icon_raw).first()
            item.save()
            print(f'{index+1}/{count}')

