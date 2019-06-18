import functools, re
from datetime import datetime, timedelta

import psycopg2
import numpy as np

def sprint_date_ranges():
    t = datetime.today()
    this_week_monday = t - timedelta(days=t.weekday())
    last_week_monday = this_week_monday - timedelta(days=7)
    this_week_sunday = this_week_monday + timedelta(days=6)
    next_week_sunday = this_week_sunday + timedelta(days=7)
    return (last_week_monday, this_week_sunday), (this_week_monday, next_week_sunday)


class C3Jira(object):
    def __init__(self, db_info):
        self.db_info = db_info
        self.db_conn = psycopg2.connect(**self.db_info)

        # Store current sprint's name
        for range in sprint_date_ranges():
            start = range[0].strftime('%b %d').upper()
            end = range[1].strftime('%b %d').upper()
            cond = "'Sprint % ({})'".format(start + ' - ' + end)

            c = self.db_conn.cursor()
            c.execute('SELECT sprint FROM c3_2_jira_tickets_history WHERE sprint LIKE {} LIMIT 1'.format(cond))
            data = np.array(c.fetchone())
            if data:
                self.curr_sprint_name = data[0]
            c.close()
        try:
            self.curr_sprint_name
        except:
            raise ValueError('Could not find the current sprint!')
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_conn.close()


    def run_sql(self, *conds):
        c = self.db_conn.cursor()

        # TODO: improve this code to prevent SQL injection
        query = '''
        SELECT *
        FROM (
            SELECT max(id) AS id, jiraid
            FROM c3_2_jira_tickets_history GROUP BY jiraid
        ) AS x INNER JOIN c3_2_jira_tickets_history AS c
        ON c.id = x.id AND c.jiraid = x.jiraid
        WHERE {};
        '''.format(' AND '.join(conds))

        c.execute(query)
        result_data = np.array(c.fetchall())

        c.close()
        return result_data


    # External methods for clients to use
    def current_issues_with_status(self, user, status = ['Done', 'Resolved', 'Closed', 'Closed-Verified']):
        conds = []
        conds.append("sprint = '{}'".format(self.curr_sprint_name))
        conds.append("assignee = '{}'".format(user))
        assigned = self.run_sql(*conds)
        
        conds.append("status IN ({})".format(', '.join(map(lambda x: "'" + x + "'", status))))
        completed = self.run_sql(*conds)
        return completed, assigned
    
    def current_issues_with_priority(self, user, priority = 'p0'):
        priorities = {
            'p0': 'P0 - Blocker',
            'p1': 'P1 - Urgent with no workaround',
            'p2': 'P2 - Critical, but workaround exists',
            'p3': 'P3 - Nice to fix',
            'p4': 'P4 - Minor',
            'other': 'Unprioritized'
        }

        conds = []
        conds.append("sprint = '{}'".format(self.curr_sprint_name))
        conds.append("assignee = '{}'".format(user))
        conds.append("priority = '{}'".format(priorities[priority]))
        assigned = self.run_sql(*conds)

        conds.append("status IN ('Canceled', 'Resolved', 'Closed', 'Closed-Verified')")
        completed = self.run_sql(*conds)
        return completed, assigned

    def current_issues_completed_rca(self, user):
        conds = []
        conds.append("sprint = '{}'".format(self.curr_sprint_name))
        conds.append("assignee = '{}'".format(user))
        conds.append("priority IN ('P0 - Blocker', 'P1 - Urgent with no workaround')")
        total = self.run_sql(*conds)

        conds.append("rca <> 'None'")
        completed = self.run_sql(*conds)
        return completed, total

    def current_issues_underestimated(self, user):
        conds = []
        conds.append("sprint = '{}'".format(self.curr_sprint_name))
        conds.append("assignee = '{}'".format(user))
        conds.append("originalestimate IS NOT NULL")
        assigned = self.run_sql(*conds)

        conds.append("timespent > originalestimate")
        underestimated = self.run_sql(*conds)
        return underestimated, assigned

    def current_sprint_num(self):
        sprint_num_match = re.search(r'(?<=Sprint )\d+', self.curr_sprint_name)
        if sprint_num_match:
            return sprint_num_match.group()
        else:
            raise ValueError('Current sprint number does not exist!')

