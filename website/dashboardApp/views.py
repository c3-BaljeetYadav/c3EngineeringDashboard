from django.views.generic import TemplateView
from django.db.models import Sum, Max
from django.contrib.auth import authenticate

import operator
from django.db.models import Q
from functools import reduce
from .models import JiraStatistics
from .data import data
# from .charts import BrowserUsageHorizontalChart


class IndexView(TemplateView):
    template_name = 'ui-template/pages/index.html'

    def get_context_data(self, **kwargs):
        # data.load_all_data()

        user = 'aiden.tai'

        sprint_obj = JiraStatistics.objects.filter(User=user).latest('SprintNum')

        def get_sprint_num():
            return '{}'.format(sprint_obj.SprintNum)

        def get_sprint_completion_rate():
            return '{:.0%}'.format(sprint_obj.SprintCompleted / sprint_obj.SprintAssigned)

        def get_sprint_completion_subscript():
            return '{!s} / {!s}'.format(sprint_obj.SprintCompleted, sprint_obj.SprintAssigned)

        def get_rca_written_or_not():
            return '{} / {}'.format(sprint_obj.RcaCompleted, sprint_obj.RcaTotal)

        def get_p0s():
            return '{!s} / {!s}'.format(sprint_obj.P0Completed, sprint_obj.P0Assigned)

        def get_p1s():
            return '{!s} / {!s}'.format(sprint_obj.P1Completed, sprint_obj.P1Assigned)

        def get_rate_under_estimated():
            return '{:.0%}'.format(sprint_obj.UnderestimatedTicketRates)

        def get_links():
            return {
                'p0':'https://c3energy.atlassian.net/issues/?filter=35273',
                'p1': 'https://c3energy.atlassian.net/issues/?filter=35274',
                'rca': 'https://c3energy.atlassian.net/issues/?filter=34972'
            }

        context = super(IndexView, self).get_context_data(**kwargs)
        context['sprint_num'] = get_sprint_num()
        context['sprint_completion'] = get_sprint_completion_rate()
        context['sprint_completion_subscript'] = get_sprint_completion_subscript()
        context['rca_written_or_not'] = get_rca_written_or_not()
        context['p0s'] = get_p0s()
        context['p1s'] = get_p1s()
        context['rate_under_estimated'] = get_rate_under_estimated()
        context['links'] = get_links()

        context['sprint_completion_chart_data'] = JiraStatistics.objects.filter(SprintNum__gte=sprint_obj.SprintNum - 10)
        return context


class LoginView(TemplateView):
    template_name = 'ui-template/pages/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context
