from typing import Any

from django.views.generic import TemplateView

from stalker_op22_cyclic_quest_wiki.models import Item
from stalker_op22_cyclic_quest_wiki.services.items.where_need import get_item_usages


class WhereItemNeededView(TemplateView):
    template_name = "wiki/items/where_needed.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        item_id = kwargs["item_id"]
        item = Item.objects.get(id=item_id)
        data = get_item_usages(item)
        base_context = super().get_context_data(**kwargs)
        return {
            **base_context,
            "where_find_info": data,
        }
