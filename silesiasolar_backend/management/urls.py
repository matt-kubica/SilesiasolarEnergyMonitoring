from django.urls import path, include
from .api import UserLocationAPI, UserMeterAPI

urlpatterns = [
    path('locations', UserLocationAPI.as_view()),
    path('meters', UserMeterAPI.as_view()),

    # path('meter', MeterAPI.as_view()),
    # path('node', NodeAPI.as_view()),
]