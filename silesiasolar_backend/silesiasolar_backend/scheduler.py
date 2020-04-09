import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from influx_updater.utils import updated_influx


scheduler = None


def start():
    # job store, for now, is unnecessary, so background scheduler dont need config
    # scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
    scheduler = BackgroundScheduler()

    logging.getLogger('apscheduler')

    scheduler.add_job(updated_influx, trigger='cron', minute="*/1")
    scheduler.start()