import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings


scheduler = None
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)

def log_hello_world():
    test_logger.debug("Hello World!")


def start():
    scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(log_hello_world, trigger='cron', minute="*/5")
    scheduler.start()