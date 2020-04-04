from django.apps import AppConfig
from django.conf import settings

class InfluxUpdaterConfig(AppConfig):
    name = 'influx_updater'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
           scheduler.start()

