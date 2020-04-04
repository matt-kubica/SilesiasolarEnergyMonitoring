from django.urls import path

from .api import LocationAPI, MeterAPI, UserAPI, DetailUserAPI

urlpatterns = [
    path('admin/locations', LocationAPI.as_view()),
    path('admin/meters', MeterAPI.as_view()),
    path('admin/users', UserAPI.as_view()),
    path('admin/users/<int:pk>', DetailUserAPI.as_view())
]