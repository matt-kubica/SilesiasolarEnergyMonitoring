from django.urls import path, include
from .api import LocationAPI, AssignedMeasurementAPI, MeterAPI, HostAPI, MeasurementDetailByMeterAPI

urlpatterns = [
    path('user/locations', LocationAPI.as_view()),
    path('user/hosts/<int:host_id>/measurements', AssignedMeasurementAPI.as_view()),
    path('user/hosts', HostAPI.as_view()),

    path('meters/<str:meter_id>/measurements', MeasurementDetailByMeterAPI.as_view()),
    path('meters', MeterAPI.as_view()),



]