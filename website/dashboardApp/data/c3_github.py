import functools, re, requests, json, urllib
from datetime import datetime, timedelta

import psycopg2
import numpy as np

from dashboardApp.models import UserProfile


def get_github_username_from_username(user):
    return UserProfile.objects.get(username=user).GithubUser


class C3Github(object):
    def __init__(self, db_info):
        self.db_info = db_info
        self.db_conn = psycopg2.connect(**self.db_info)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_conn.close()


    def run_sql(self, *conds, targets=['*']):
        c = self.db_conn.cursor()

        # TODO: improve this code to prevent SQL injection
        query = '''
        SELECT {}
        FROM (
            SELECT max(id) AS id, pull_id
            FROM c3_2_github_pulls GROUP BY pull_id
        ) AS x INNER JOIN c3_2_github_pulls AS c
        ON c.id = x.id AND c.pull_id = x.pull_id
        WHERE {};
        '''.format(
            ','.join(map(lambda x: 'c.' + x, targets)),
            ' AND '.join(conds)
        )

        c.execute(query)
        result_data = np.array(c.fetchall())

        c.close()
        return result_data


    # External methods for clients to use
    def pr_over_24_hours(self, user):
        username = get_github_username_from_username(user)
        
        conds = []
        conds.append("username = '{}'".format(username))
        conds.append("updated_at < GETDATE() - '1 day'::INTERVAL")
        prs = self.run_sql(*conds, targets=['pull_id', 'title'])

        result = []
        for i in range(prs.shape[0]):
            r = {'User': user}
            r['Number'] = prs[i, 0]
            r['Title'] = prs[i, 1]
            r['Url'] = 'https://github.com/c3-e/c3server/pull/' + r['Number']
            r['id'] = r['User'] + '_' + str(r['Number'])
            result.append(r)
        return result


    def pr_size(self, user):
        username = get_github_username_from_username(user)

        # Get all repos associated with this username
        c = self.db_conn.cursor()
        c.execute("SELECT DISTINCT repo FROM c3_2_github_pulls WHERE username = '{}';".format(username))
        repos = list(c.fetchall())
        repos = map(lambda x: x[0], repos)
        c.close()

        user_prs = []
        for r in repos:
            conds = []
            conds.append("username = '{}'".format(username))
            conds.append("repo = '{}'".format(r))
            prs = self.run_sql(*conds, targets=['pull_id', 'additions', 'deletions'])

            for i in range(prs.shape[0]):
                result_pr = {'id': user + '_' + r, 'User': user, 'Repo': r}
                result_pr['Number'] = prs[i, 0]
                result_pr['Additions'] = prs[i, 1]
                result_pr['Deletions'] = prs[i, 2]
                user_prs.append(result_pr)
        return user_prs
