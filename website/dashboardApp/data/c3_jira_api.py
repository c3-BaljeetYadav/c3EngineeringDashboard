import requests
import functools
import re
from jira import JIRA


# Idea from https://github.com/r3ap3rpy/python/blob/master/JiraAPIWrapper.py
class JiraException(Exception):
    pass


class C3Jira(object):
    # Overwriting default methods
    def __init__(self, **kwargs):
        if len(kwargs) != 3:
            raise JiraException('In order to use this class you need to specify a server, a user, and a token as keyword arguments!')
        else:
            if 'server' in kwargs.keys():
                self.__options = {
                    'server': kwargs['server'],
                    'verify': True
                }
            else:
                raise JiraException('You need to specify a server as keyword argument!')

            if 'username' in kwargs.keys():
                self.__username = kwargs['username']
            else:
                raise JiraException('You need to specify a username as keyword argument!')

            if 'token' in kwargs.keys():
                self.__token = kwargs['token']
            else:
                raise JiraException('You need to specify a token as keyword argument!')
            
            try:
                self.__client = JIRA(self.__options, basic_auth=(self.__username, self.__token))
            except:
                raise JiraException('Could not connect to the API, invalid username or token!') from None
            
            # Save my current sprint's issues once to save loading time
            self.curr_issues = self.__client.search_issues('sprint in openSprints() AND assignee = currentUser()')

    def __str__(self):
        return 'Jira(username = {}, token = {}, endpoint = {}'.format(self.__username, self.__token, self.__options['server'])

    def __repr__(self):
        return 'Jira(username = {}, token = {}, endpoint = {}'.format(self.__username, self.__token, self.__options['server'])

    def __format__(self, r):
        return 'Jira(username = {}, token = {}, endpoint = {}'.format(self.__username, self.__token, self.__options['server'])


    # Helper methods
    def my_current_issues_with(self, equals = {}, inequals = {}):
        # equals and inequals is expected to be a dictionary with field -> value
        def field_equal(f, i, tf):
            if hasattr(getattr(i.fields, f), 'id') and hasattr(tf, 'id') and getattr(i.fields, f).id == tf.id:
                return True
            else:
                return getattr(i.fields, f) == tf

        result_issues = []
        for issue in self.curr_issues:
            if (
                all((field_equal(field, issue, equals[field]) for field in equals)) and
                all((not field_equal(field, issue, inequals[field]) for field in inequals))
            ):
                result_issues.append(issue)
        return result_issues


    # External methods for clients to use
    def current_issues_with_status(self, status = ['Done', 'Resolved', 'Closed', 'Closed-Verified']):
        status_list = {
            'Open': '1',
            'Resolved': '10104',
            'In Review': '10001',
            'Backlog': '10002',
            'Selected for Development': '10003',
            'Spec in Progress': '10200',
            'Specification Complete': '10201',
            'Abandoned': '10272',
            'Approval': '10273',
            'Final Approval': '10274',
            'To Do': '10005',
            'Done': '10004',
            'In Progress': '3',
            'Reopened': '4',
            'Closed': '5',
            'Closed-Verified': '6'
        }
        completed = []
        for s in status:
            status_id = self.__client.status(status_list[s])
            completed.extend(self.my_current_issues_with(equals={'status': status_id}))
        return completed, self.curr_issues
    
    def current_issues_with_priority(self, priority = 'p0'):
        priorities = {
            'p0': '1',
            'p1': '2',
            'p2': '3',
            'p3': '4',
            'p4': '5',
            'other': '6'
        }
        priority_id = self.__client.priority(priorities[priority])
        assigned = self.my_current_issues_with(equals={'priority': priority_id})
        completed = []
        for issue in assigned:
            if str(issue.fields.status) in ['Canceled', 'Resolved', 'Closed']:
                completed.append(issue)
        return completed, assigned

    def current_num_completed_rca(self):
        # Root cause assessment
        rca = 'customfield_13100'
        return len(self.my_current_issues_with(inequals={rca: 'None'}))

    def current_rate_underestimated_tickets(self):
        num_underestimated = num_completed_with_estimate = 0
        for issue in self.curr_issues:
            if issue.fields.timeoriginalestimate and issue.fields.timespent:
                num_completed_with_estimate += 1
                if int(issue.fields.timeoriginalestimate) < int(issue.fields.timespent):
                    num_underestimated += 1
        return num_underestimated / num_completed_with_estimate if num_completed_with_estimate != 0 else 0.0
    
    def current_sprint_num(self):
        if self.curr_issues:
            # TODO: replace hardcoded sprint source with something more flexible (customfield_10782)
            sprint_info = self.curr_issues[0].fields.customfield_10782[0]
            sprint_num_match = re.search('(?<=name\=Sprint )\d+', sprint_info)
            if sprint_num_match:
                return sprint_num_match.group()
            else:
                raise ValueError('Current sprint number does not exist!')
        else:
            return 0


if __name__ == '__main__':
    pass_file_name = 'jira.pass'
    with open(pass_file_name) as f:
        username, token = [s.strip() for s in f]

    jira = C3Jira(server='https://c3energy.atlassian.net', username=username, token=token)

    status = ['Done', 'Resolved', 'Closed', 'Closed-Verified']
    print('Sprint completion:', jira.current_issues_with_status(status))


    print('P0:', jira.current_issues_with_priority('p0'))
    print('P1:', jira.current_issues_with_priority('p1'))

    print('# of RCAs completed:', jira.current_num_completed_rca())

    print('% of underestimated tickets:', jira.current_rate_underestimated_tickets())
