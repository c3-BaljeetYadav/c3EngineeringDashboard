import os
from collections import defaultdict
from datetime import datetime, timedelta

from dashboardApp.models import JiraStatistics, GithubPullRequestSize, GithubPullRequestNotification
from dashboardApp.models import UserProfile
from django.db import IntegrityError

from .c3_jira import C3Jira
from .c3_github import C3Github


def update_jira_stats(db_info):
    result_stats = {}
    jira = C3Jira(db_info)
    users = UserProfile.objects.all().filter(is_staff=False)

    for user_info in users:
        user = user_info.username

        result_stats['User'] = user
        result_stats['SprintNum'] = jira.current_sprint_num()
        result_stats['id'] = result_stats['User'] + '_' + str(result_stats['SprintNum'])

        sprint_completed, sprint_assigned = jira.current_issues_with_status(user, ['Done', 'Resolved', 'Closed', 'Closed-Verified'])
        p0_completed, p0_assigned = jira.current_issues_with_priority(user, 'p0')
        p1_completed, p1_assigned = jira.current_issues_with_priority(user, 'p1')
        result_stats['SprintCompleted'] = len(sprint_completed)
        result_stats['SprintAssigned'] = len(sprint_assigned)
        result_stats['P0Completed'] = len(p0_completed)
        result_stats['P0Assigned'] = len(p0_assigned)
        result_stats['P1Completed'] = len(p1_completed)
        result_stats['P1Assigned'] = len(p1_assigned)

        rca_completed, rca_total = jira.current_issues_completed_rca(user)
        underestimated, time_total = jira.current_issues_underestimated(user)
        result_stats['RcaCompleted'] = len(rca_completed)
        result_stats['RcaTotal'] = len(rca_total)
        result_stats['UnderestimatedTicketRates'] = len(underestimated) / len(time_total)

        j = JiraStatistics(**result_stats)
        if JiraStatistics.objects.filter(id = result_stats['id']).count():
            j.save(force_update=True)
        else:
            j.save()


def update_github_info(db_info):
    github = C3Github(db_info)
    users = UserProfile.objects.all().filter(is_staff=False)

    GithubPullRequestNotification.objects.all().delete()

    for user_info in users:
        user = user_info.username

        # Size of pull requests
        prs_size = github.pr_size(user)
        for p in prs_size:
            g = GithubPullRequestSize(**p)
            if GithubPullRequestSize.objects.filter(id = p['id']).count():
                g.save(force_update=True)
            else:
                g.save()

        # Pull requests over 24 hours
        prs_24_hours = github.pr_over_24_hours(user)
        for p in prs_24_hours:
            g = GithubPullRequestNotification(**p)
            g.save()


def load_all_data():
    try:
        username, password = os.environ['C3P0_USERNAME'], os.environ['C3P0_PASSWORD']
    except:
        raise Exception('You need to set environment variables: C3P0_USERNAME, C3P0_PASSWORD')

    db_info = {
        'dbname': 'prodc3rs01',
        'host': 'stage-c3-rs-01.c7kp1i36dopx.us-east-1.redshift.amazonaws.com',
        'port': '5439',
        'user': username,
        'password': password
    }
    update_jira_stats(db_info)
    update_github_info(db_info)

    print('All data successfully fetched and saved!')
