import sqlite3
from c3_jira_api import C3Jira


def get_jira_stats():
    result_stats = {}

    pass_file_name = 'login_info.pass'
    with open(pass_file_name) as f:
        username, token = [s.strip() for s in f]

    jira = C3Jira(server='https://c3energy.atlassian.net', username=username, token=token)

    result_stats['SprintNum'] = jira.current_sprint_num()

    p0_completed, p0_assigned = jira.current_issues_with_priority('p0')
    p1_completed, p1_assigned = jira.current_issues_with_priority('p1')
    result_stats['P0Completed'] = len(p0_completed)
    result_stats['P0Assigned'] = len(p0_assigned)
    result_stats['P1Completed'] = len(p1_completed)
    result_stats['P1Assigned'] = len(p1_assigned)

    result_stats['SprintCompletionRates'] = jira.current_rate_with_status(['Canceled', 'Resolved', 'Closed'])
    result_stats['NumberOfCompletedRcas'] = jira.current_num_completed_rca()
    result_stats['UnderestimatedTicketRates'] = jira.current_rate_underestimated_tickets()

    return result_stats


def save_stats_to_db(stats, db_name, table_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    col_names = list(stats.keys())
    new_row = list(stats.values())

    # Create new table if the specified database does not exist
    c.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name="{}"'.format(table_name))
    if c.fetchone()[0] == 0:
        c.execute('CREATE TABLE {} ({});'.format(table_name, ','.join(col_names)))
    else:
        print('table already exists')
        c.execute('SELECT * FROM {};'.format(table_name))
        if len(c.description) != len(stats):
            raise ValueError('The number of statistics does not match the ones in the database!')

    # TODO: improve for security (e.g. SQL injection)
    c.execute('INSERT INTO {} ({}) VALUES ({});'.format(table_name, ','.join(col_names), ','.join(str(x) for x in new_row)))
    conn.commit()
    conn.close()



if __name__ == '__main__':
    stats = get_jira_stats()
    db_name = 'jira.db'
    table_name = 'Statistics'
    save_stats_to_db(stats, db_name, table_name)

    print('Data successfully saved!')
