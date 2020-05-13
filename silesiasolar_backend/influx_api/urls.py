from django.urls import path
from .api import hello_influx_api, get_current

urlpatterns = [
    path('influx_api/hello', hello_influx_api),
    path('influx_api/get_current', get_current),
]