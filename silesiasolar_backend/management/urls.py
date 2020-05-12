from django.urls import path, include
from .api import LocationAPI, ChosenMeasurementsAPI, MeterAPI, HostAPI, MeasurementAPI

urlpatterns = [
    path('locations', LocationAPI.as_view()),
    path('hosts/<int:host_id>/measurements', ChosenMeasurementsAPI.as_view()),

    path('meters', MeterAPI.as_view()),
    path('hosts', HostAPI.as_view()),
    path('measurements', MeasurementAPI.as_view())


]