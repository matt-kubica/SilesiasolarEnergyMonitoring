from django.urls import path, include
from .api import UserLocationAPI, UserMeterAPI, AdminMeterAPI

urlpatterns = [
    path('locations', UserLocationAPI.as_view()),
    path('meters', UserMeterAPI.as_view()),
    path('admin/meters', AdminMeterAPI.as_view())

    # path('meter', MeterAPI.as_view()),
    # path('node', NodeAPI.as_view()),
]