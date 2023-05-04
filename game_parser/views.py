from django.views.generic import TemplateView

from game_parser.logic.tasks_grouping import collect_info


class TasksListView(TemplateView):

    template_name = 'vendors_tasks_list.html'

    def get_context_data(self, **kwargs):
        data = collect_info()
        return {'vendors_quests': data}
