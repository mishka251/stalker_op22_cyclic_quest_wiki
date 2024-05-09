from typing import Any

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "wiki/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "meta_description": "Энциклопедия по сталкер ОП-2.2",
            "meta_keywords": "сталкер, stalker, объединенный пак 2.2, циклические квесты, ОП-2.2",
        }
