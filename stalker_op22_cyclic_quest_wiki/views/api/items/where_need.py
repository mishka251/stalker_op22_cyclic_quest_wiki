from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views import View

from stalker_op22_cyclic_quest_wiki.models import Item
from stalker_op22_cyclic_quest_wiki.services.items.where_need import get_item_usages


class WhereNeedItemAPI(View):

    def get(self, request: HttpRequest, **kwargs: Any) -> JsonResponse:
        item_id = kwargs["item_id"]
        item = Item.objects.get(id=item_id)
        data = get_item_usages(item)
        return JsonResponse(data.to_json(), safe=False)
