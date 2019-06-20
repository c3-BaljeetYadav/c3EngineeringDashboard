import requests, json
import functools, re, requests, json, urllib
from datetime import datetime, timedelta

import psycopg2
import numpy as np

from dashboardApp.models import UserProfile


def get_github_names_from_username(user):
    github_username = UserProfile.objects.get(username=user).GithubUser
    api_url = 'https://api.github.com/users/{}'.format(github_username)
    r = requests.get(api_url, auth=('c3p0-c3p0', 'd10032c59bf649a5240ec3c7dddb85a9439c3251'))
    if r.ok:
        user_json = json.loads(r.text or r.content)
        github_name = user_json['name']
        if not github_name:
            github_name = github_username
    else:
        raise ValueError('Connection to Github API failed for: ' + github_username)
    return github_username, github_name


class C3Github(object):
    def __init__(self, db_info):
        self.db_info = db_info
        self.db_conn = psycopg2.connect(**self.db_info)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_conn.close()

    def run_sql(self, query):
        c = self.db_conn.cursor()
        c.execute(query)
        result_data = np.array(c.fetchall())
        c.close()
        return result_data

    def run_sql_github(self, *conds, targets=['*']):
        # TODO: improve this code to prevent SQL injection
        query = '''
        SELECT {}
        FROM c3_2_github_pulls
        WHERE {};
        '''.format(
            ','.join(targets),
            ' AND '.join(conds)
        )
        return self.run_sql(query)

    def run_sql_jira(self, *conds, targets=['*']):
        # TODO: improve this code to prevent SQL injection
        query = '''
        SELECT {}
        FROM (
            SELECT max(created) AS ldate, pullrequests_id AS pid, branches_repository_name AS repo
            FROM c3_2_jira_github_requests GROUP BY pullrequests_id, branches_repository_name
        ) AS x INNER JOIN c3_2_jira_github_requests AS c
        ON c.pullrequests_id = x.pid AND c.created = x.ldate AND c.branches_repository_name = x.repo
        WHERE {};
        '''.format(
            ','.join(map(lambda x: 'c.' + x, targets)),
            ' AND '.join(map(lambda x: 'c.' + x, conds))
        )
        return self.run_sql(query)


    # External methods for clients to use
    def pr_over_24_hours(self, user):
        _, github_name = get_github_names_from_username(user)

        result = []
        query = '''
        SELECT g.pull_id, g.title
        FROM c3_2_github_pulls AS g
        WHERE (
            SELECT COUNT(*)
            FROM (
                SELECT max(created) AS ldate, pullrequests_id AS pid, branches_repository_name AS repo
                FROM c3_2_jira_github_requests GROUP BY pullrequests_id, branches_repository_name
            ) AS x INNER JOIN c3_2_jira_github_requests AS j
            ON j.pullrequests_id = x.pid AND j.created = x.ldate AND j.branches_repository_name = x.repo

            WHERE j.pullrequests_reviewers_name = '{}'
            AND j.pullrequests_lastupdate < GETDATE() - '1 day'::INTERVAL
            AND j.pullrequests_status = 'OPEN'

            AND g.pull_id = j.pullrequests_id
            AND g.repo = j.branches_repository_name
        ) > 1
        '''.format(github_name)
        prs = self.run_sql(query)

        for i in range(prs.shape[0]):
            r = {'User': user}
            r['Number'] = prs[i, 0][1:]
            r['Title'] = prs[i, 1]
            r['Url'] = 'https://github.com/c3-e/c3server/pull/' + r['Number']
            r['id'] = r['User'] + '_' + str(r['Number'])
            result.append(r)
        return result


    def pr_size(self, user):
        _, github_name = get_github_names_from_username(user)

        result = []
        query = '''
        SELECT g.repo, g.additions, g.deletions, g.pull_id
        FROM c3_2_github_pulls AS g
        WHERE (
            SELECT COUNT(*)
            FROM c3_2_jira_github_requests AS j
            WHERE j.pullrequests_author_name = '{}'

            AND g.pull_id = j.pullrequests_id
            AND g.repo = j.branches_repository_name
        ) > 1
        '''.format(github_name)

        prs = self.run_sql(query)

        for i in range(prs.shape[0]):
            result_pr = {'User': user}
            result_pr['Repo'] = prs[i, 0]
            result_pr['Additions'] = prs[i, 1]
            result_pr['Deletions'] = prs[i, 2]
            result_pr['Number'] = prs[i, 3][1:]
            result_pr['id'] = result_pr['User'] + '_' + result_pr['Repo'] + '_' + result_pr['Number']
            result.append(result_pr)
        return result
