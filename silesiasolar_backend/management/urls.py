from django.urls import path, include
from .api import LocationAPI

urlpatterns = [
    path('location', LocationAPI.as_view()),
    # path('meter', MeterAPI.as_view()),
    # path('node', NodeAPI.as_view()),
]