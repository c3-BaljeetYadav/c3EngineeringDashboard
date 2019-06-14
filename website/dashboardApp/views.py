# from django.http import HttpResponse
#
#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.views.generic import TemplateView
from django.db.models import Sum, Max
import operator
from django.db.models import Q
from functools import reduce
# from .models import JiraLogSprintCompletion, JiraLogs
from .models import JiraStatistics
from .data import data
from .charts import BrowserUsageHorizontalChart

HOURS_IN_SPRINT = 80

class NewsView(TemplateView):
    template_name = 'ui-template/pages/news.html'

    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        return context

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        # Instantiate our chart. We'll keep the size/style/etc.
        # config here in the view instead of `charts.py`.
        # cht_fruits = FruitPieChart(
        #     height=600,
        #     width=800,
        #     explicit_size=True,
        #     style=DarkStyle
        # )

        cht_browsers = BrowserUsageHorizontalChart(
            height=600,
            width=800,
            explicit_size=True,
            # style=DarkStyle
        )
        # Call the `.generate()` method on our chart object
        # and pass it to template context.
        # context['cht_fruits'] = cht_fruits.generate()
        context['cht_browsers'] = cht_browsers.generate()
        return context


class SingleView(TemplateView):
    template_name = 'ui-template/pages/index.html'

    def get_context_data(self, **kwargs):
        data.load_all_data()
        sprint_obj = JiraStatistics.objects.latest('SprintNum')

        def get_sprint_completion_rate():
            return '{:.0%}'.format(sprint_obj.SprintCompleted / sprint_obj.SprintAssigned)

        def get_sprint_completion_subscript():
            return '{!s} / {!s}'.format(sprint_obj.SprintCompleted, sprint_obj.SprintAssigned)

        def get_rca_written_or_not():
            return '{}'.format(sprint_obj.NumberOfCompletedRcas)

        def get_p0s():
            return '{!s} / {!s}'.format(sprint_obj.P0Completed, sprint_obj.P0Assigned)

        def get_p1s():
            return '{!s} / {!s}'.format(sprint_obj.P1Completed, sprint_obj.P1Assigned)

        def get_rate_under_estimated():
            return '{:.0%}'.format(sprint_obj.UnderestimatedTicketRates)

        def get_p0_filter_link():
            return '#'

        context = super(SingleView, self).get_context_data(**kwargs)
        context['sprint_completion'] = get_sprint_completion_rate()
        context['sprint_completion_subscript'] = get_sprint_completion_subscript()
        context['rca_written_or_not'] = get_rca_written_or_not()
        context['p0s'] = get_p0s()
        context['p1s'] = get_p1s()
        context['rate_under_estimated'] = get_rate_under_estimated()
        context['p0_filter'] = get_p0_filter_link()
        return context


class LoginView(TemplateView):
    template_name = 'ui-template/index-okta.html.en'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context;
