from typing import cast

from django.db.models import Q, QuerySet
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.generic.list import MultipleObjectMixin

from stalker_op22_cyclic_quest_wiki.models import Item
from stalker_op22_cyclic_quest_wiki.views.items.list import SearchForm


class ItemsSearchAPI(MultipleObjectMixin, View):
    paginate_by = 35
    ordering = "name_translation__rus"
    allow_empty = True

    model = Item

    def get_queryset(self) -> QuerySet[Item]:
        qs: QuerySet[Item] = cast(QuerySet[Item], super().get_queryset())
        search_form = self.get_search_form()
        if search_form.is_valid():
            search = search_form.cleaned_data["search"]
            qs = qs.filter(
                Q(name__icontains=search) | Q(name_translation__rus__icontains=search),
            )
        return qs

    def get_search_form(self) -> SearchForm:
        return SearchForm(self.request.GET)

    def get(self, request: HttpRequest) -> JsonResponse:
        context = self.get_context_data(object_list=self.get_queryset())
        data = {
            "items": [self._item_to_json(item) for item in context["page_obj"]],
            "paginator": {
                "page": context["page_obj"].number,
                "total": context["paginator"].count,
                "num_pages": context["paginator"].num_pages,
            },
        }
        return JsonResponse(data, safe=False)

    def _item_to_json(self, item: Item) -> dict:
        return {
            "name": {
                "rus": item.name_translation.rus,
            },
            "icon": {
                "url": item.icon.icon.url,
                "width": item.icon.icon.width,
                "height": item.icon.icon.height,
            },
            "code": item.name,
            "id": str(item.id),
        }
