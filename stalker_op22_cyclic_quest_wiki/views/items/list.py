from typing import Any, cast

from django.db.models import Q, QuerySet
from django.forms import CharField, Form
from django.views.generic import ListView

from stalker_op22_cyclic_quest_wiki.models import Item


class SearchForm(Form):
    search = CharField(required=False, label="Поиск")


class ItemsListView(ListView):
    template_name = "wiki/items/items_list.html"
    paginate_by = 35
    ordering = "name_translation__rus"
    allow_empty = True

    model = Item

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_form = self.get_search_form()
        return {
            **context,
            "search_form": search_form,
        }

    def get_search_form(self) -> SearchForm:
        return SearchForm(self.request.GET)

    def get_queryset(self) -> QuerySet[Item]:
        qs: QuerySet[Item] = cast(QuerySet[Item], super().get_queryset())
        search_form = self.get_search_form()
        if search_form.is_valid():
            search = search_form.cleaned_data["search"]
            qs = qs.filter(
                Q(name__icontains=search) | Q(name_translation__rus__icontains=search),
            )
        return qs
