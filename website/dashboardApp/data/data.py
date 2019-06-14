from collections import defaultdict
from datetime import datetime, timedelta

from github import Github
from dashboardApp.models import JiraStatistics, GithubPullRequestSize, GithubPullRequestNotification

from .c3_jira_api import C3Jira


def get_jira_stats(username, token):
    result_stats = {}

    jira = C3Jira(server='https://c3energy.atlassian.net', username=username, token=token)

    result_stats['SprintNum'] = jira.current_sprint_num()

    sprint_completed, sprint_assigned = jira.current_issues_with_status(['Done', 'Resolved', 'Closed', 'Closed-Verified'])
    p0_completed, p0_assigned = jira.current_issues_with_priority('p0')
    p1_completed, p1_assigned = jira.current_issues_with_priority('p1')
    result_stats['SprintCompleted'] = len(sprint_completed)
    result_stats['SprintAssigned'] = len(sprint_assigned)
    result_stats['P0Completed'] = len(p0_completed)
    result_stats['P0Assigned'] = len(p0_assigned)
    result_stats['P1Completed'] = len(p1_completed)
    result_stats['P1Assigned'] = len(p1_assigned)

    result_stats['NumberOfCompletedRcas'] = jira.current_num_completed_rca()
    result_stats['UnderestimatedTicketRates'] = jira.current_rate_underestimated_tickets()

    return result_stats


def save_stats_to_db(stats):
    j = JiraStatistics(**stats)
    j.save()


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
    jira_pass_fname = 'dashboardApp/data/jira.pass'
    with open(jira_pass_fname) as f:
        jira_username, jira_token = [s.strip() for s in f]

    stats = get_jira_stats(jira_username, jira_token)
    save_stats_to_db(stats)

    github_pass_fname = 'dashboardApp/data/github.pass'
    with open(github_pass_fname) as f:
        github_username, github_token = [s.strip() for s in f]

    pr_sizes, pr_notify = get_github_info(github_username, github_token)
    save_github_info_to_db(pr_sizes, pr_notify)
    print('All data successfully fetched and saved!')
