from django_cron import CronJobBase, Schedule
from .data import data

class UpdateData(CronJobBase):
    RUN_EVERY_MINS = 60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dashboardApp.update_data'

    def do(self):
        data.load_all_data()
