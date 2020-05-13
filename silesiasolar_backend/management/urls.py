from django.urls import path, include
from .api import LocationAPI, ChosenMeasurementsAPI, MeterAPI, HostAPI, MeasurementDetailByMeterAPI

urlpatterns = [
    path('user/locations', LocationAPI.as_view()),
    path('user/hosts/<int:host_id>/measurements', ChosenMeasurementsAPI.as_view()),
    path('user/hosts', HostAPI.as_view()),

    path('meters/<int:meter_id>/measurements', MeasurementDetailByMeterAPI.as_view()),
    path('meters', MeterAPI.as_view()),



]