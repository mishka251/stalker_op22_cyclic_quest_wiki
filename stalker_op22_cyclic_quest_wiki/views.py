from django.shortcuts import render
from django.views.generic import TemplateView

from stalker_op22_cyclic_quest_wiki.models.base.character import Character


class QuestChartersListView(TemplateView):
    template_name = 'characters_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        characters = Character.objects.all()
        return context_data

# Create your views here.
class CyclicQuestsView(TemplateView):
    ...

