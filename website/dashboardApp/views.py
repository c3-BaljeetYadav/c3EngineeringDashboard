from django.views.generic import TemplateView
from django.db.models import Sum, Max
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

import operator
from django.db.models import Q
from functools import reduce
from .models import JiraStatistics, GithubPullRequestSize, GithubPullRequestNotification
from .data import data
from .forms import SignupForm


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'ui-template/pages/index.html'
    login_url = '/dashboard/login'

    def get_context_data(self, **kwargs):
        data.load_all_data()

        user = self.request.user

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
        
        def get_pr_size_data(num_pr):
            result = []
            repos = GithubPullRequestSize.objects.filter(User=user).order_by().values('Repo').distinct()
            for r in repos:
                prs = GithubPullRequestSize.objects.filter(User=user, Repo=r).order_by('-Number')[:num_pr][::-1]
                result.append((r, prs))
            return result

        context = super(IndexView, self).get_context_data(**kwargs)
        context['sprint_num'] = get_sprint_num()
        context['sprint_completion'] = get_sprint_completion_rate()
        context['sprint_completion_subscript'] = get_sprint_completion_subscript()
        context['rca_written_or_not'] = get_rca_written_or_not()
        context['p0s'] = get_p0s()
        context['p1s'] = get_p1s()
        context['rate_under_estimated'] = get_rate_under_estimated()
        context['links'] = get_links()

        num_pr = 50
        num_sprint = 10
        context['pull_request_notify_panel_data'] = GithubPullRequestNotification.objects.filter(User=user)
        context['pull_request_size_chart_data'] = get_pr_size_data(num_pr)
        context['sprint_completion_chart_data'] = JiraStatistics.objects.filter(User=user, SprintNum__gte=sprint_obj.SprintNum - num_sprint)
        return context


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'ui-template/pages/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
