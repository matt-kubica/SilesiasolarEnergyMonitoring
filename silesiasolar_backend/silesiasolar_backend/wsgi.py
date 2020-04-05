"""
WSGI config for silesiasolar_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from . import scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silesiasolar_backend.settings')

application = get_wsgi_application()

# scheduler must be started here since it is wsgi application,
# starting in other place would case creating multiple scheduler instances
if settings.SCHEDULER_AUTOSTART:
    scheduler.start()
