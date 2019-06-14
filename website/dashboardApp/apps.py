from django.apps import AppConfig


class DashboardappConfig(AppConfig):
    name = 'dashboardApp'
    verbose_name = 'Dashboard Application'
    def ready(self):
        pass
