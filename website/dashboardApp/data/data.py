import os
from collections import defaultdict
from datetime import datetime, timedelta

from github import Github
from dashboardApp.models import JiraStatistics, GithubPullRequestSize, GithubPullRequestNotification
from django.contrib.auth.models import User
from django.db import IntegrityError

from .c3_jira import C3Jira


def update_jira_stats(db_info):
    result_stats = {}
    jira = C3Jira(db_info)
    users = User.objects.all()

    for user_info in users:
        user = user_info.username

        result_stats['User'] = user
        result_stats['SprintNum'] = jira.current_sprint_num()

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
        try:
            j.save()
        except IntegrityError:
            pass


def get_github_info(username, token):
    g = Github(username, token)

    # Size of pull requests
    pr_sizes = defaultdict(list)
    my_repos = g.get_user().get_repos()
    for r in my_repos:
        pulls = r.get_pulls(sort='created')
        for p in pulls:
            if p.assignee == g.get_user():
                new_pr = {
                    'Number': p.number,
                    'Additions': p.additions,
                    'Deletions': p.deletions
                }
                pr_sizes[r].append(new_pr)

    # Pull requests notification that are over 24 hours
    compare_time = datetime.now() - timedelta(days=1)
    pr_notify = []
    for r in my_repos:
        pulls = r.get_pulls(state='open')
        for p in pulls:
            if p.assignee == g.get_user() and p.updated_at < compare_time:
                new_pr = {
                    'Number': p.number,
                    'Title': p.title,
                    'Url': p.html_url
                }
                pr_notify.append(new_pr)
    
    return pr_sizes, pr_notify


def save_github_info_to_db(pr_sizes, pr_notify):
    # Size of pull requests
    for repo, pr in pr_sizes.items():
        g = GithubPullRequestSize(Repo=repo, **pr)
        g.save()

    # Pull requests notification that are over 24 hours
    GithubPullRequestNotification.objects.all().delete()
    for pr in pr_notify:
        g = GithubPullRequestNotification(**pr)
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

    github_pass_fname = 'dashboardApp/data/github.pass'
    with open(github_pass_fname) as f:
        github_username, github_token = [s.strip() for s in f]

    pr_sizes, pr_notify = get_github_info(github_username, github_token)
    save_github_info_to_db(pr_sizes, pr_notify)
    print('All data successfully fetched and saved!')
