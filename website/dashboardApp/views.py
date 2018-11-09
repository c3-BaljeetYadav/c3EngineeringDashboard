# from django.http import HttpResponse
#
#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.views.generic import TemplateView
from django.db.models import Sum
import operator
from django.db.models import Q
from functools import reduce
from .models import JiraLogSprintCompletion, JiraLogs
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
        context = super(SingleView, self).get_context_data(**kwargs)
        context['sprint_completion'] = self.get_sprint_completion_rate()
        context['sprint_completion_subscript'] = self.get_sprint_completion_subscript()
        context['rca_written_or_not'] = self.get_rca_written_or_not()
        context['p0s'] = self.get_p0s()
        context['p1s'] = self.get_p1s()
        context['tickets_under_estimated'] = self.get_tickets_under_estimated()
        context['time_in_meetings_today'] = self.get_time_in_meetings_today()
        return context;

    def get_sprint_completion_rate(self, current_sprint='247', current_user='jinyan.liu'):
        sprint_objs = JiraLogSprintCompletion.objects.filter(assignee='jinyan.liu', sprint='247')
        sum = 0;
        for obj_ in sprint_objs:
            sum += float(obj_.timeSpent)
        return '%d%%' % (int(sum/HOURS_IN_SPRINT * 100));

    def get_sprint_completion_subscript(self, current_sprint='247', current_user='jinyan.liu'):
        sprint_objs = JiraLogSprintCompletion.objects.filter(assignee='jinyan.liu', sprint='247')
        sum = 0;
        for obj_ in sprint_objs:
            sum += float(obj_.timeSpent)
        return '%d / %d' % (int(sum), HOURS_IN_SPRINT);

    def get_rca_written_or_not(self):
        query_p0_p1 = reduce(operator.or_, (Q(priority__contains=x) for x in ['P0', 'P1']))
        set_one = JiraLogs.objects.filter(assignee='jinyan.liu', sprint__contains='247', issueType__contains='Bug')

        sprint_objs_needing_rca = set_one.filter(query_p0_p1)
        sprint_objs_with_rca = sprint_objs_needing_rca.exclude(rca__isnull=True).exclude(rca__exact='')
        return '%d/%d' % (len(sprint_objs_with_rca), len(sprint_objs_needing_rca))

    def get_p0s(self):
        p0_objs = JiraLogs.objects.filter(assignee='jinyan.liu', sprint__contains='247', priority__contains='P0')
        status_query = reduce(operator.or_, (Q(status__contains=x) for x in ['Closed', 'Close-Verified']))
        completed_p0s_objs = p0_objs.filter(status_query)
        return '%d/%d' % (len(completed_p0s_objs), len(p0_objs))

    def get_p1s(self):
        p1_objs = JiraLogs.objects.filter(assignee='jinyan.liu', sprint__contains='247', priority__contains='P1')
        status_query = reduce(operator.or_, (Q(status__contains=x) for x in ['Closed', 'Close-Verified']))
        completed_p1s_objs = p1_objs.filter(status_query)
        return '%d/%d' % (len(completed_p1s_objs), len(p1_objs))

    def get_tickets_under_estimated(self):
        sprint_objs = JiraLogs.objects.filter(assignee='jinyan.liu', sprint__contains='247').exclude(timeSpent__isnull=True).exclude(originalEstimate__isnull=True)
        count = 0
        for obj_ in sprint_objs:
            if obj_.timeSpent > obj_.originalEstimate:
                count += 1
        return count

    def get_time_in_meetings_today(self):
        return '%d' % (2)


class LoginView(TemplateView):
    template_name = 'ui-template/index-okta.html.en'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context;
