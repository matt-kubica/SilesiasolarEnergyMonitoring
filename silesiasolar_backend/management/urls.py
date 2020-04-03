from django.urls import path, include
from .api import UserLocationAPI

urlpatterns = [
    path('location', UserLocationAPI.as_view()),
    # path('meter', MeterAPI.as_view()),
    # path('node', NodeAPI.as_view()),
]