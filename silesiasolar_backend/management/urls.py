from django.urls import path, include
from .api import LocationAPI, ChosenMeasurementsAPI, MeterAPI, HostAPI, RegisterDetailByMeterAPI

urlpatterns = [
    path('locations', LocationAPI.as_view()),
    path('hosts/<int:host_id>/measurements', ChosenMeasurementsAPI.as_view()),
    path('meters/<int:meter_id>/registers', RegisterDetailByMeterAPI.as_view()),
    path('meters', MeterAPI.as_view()),
    path('hosts', HostAPI.as_view()),



]