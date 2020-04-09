import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from influx_updater.utils import updated_influx


scheduler = None


def start():
    # job store, for now, is unnecessary, so background scheduler dont need config
    # scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
    scheduler = BackgroundScheduler()

    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(updated_influx, trigger='cron', minute="*/1")
    scheduler.start()