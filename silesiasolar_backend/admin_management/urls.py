from django.urls import path

from .api import LocationAPI, LocationDetailAPI, HostAPI, HostDetailAPI, MeterAPI, UserAPI, UserDetailAPI, RegisterAPI, MeasurementAPI

urlpatterns = [
    path('admin/locations', LocationAPI.as_view()),
    path('admin/locations/<int:pk>', LocationDetailAPI.as_view()),

    path('admin/hosts', HostAPI.as_view()),
    path('admin/hosts/<int:pk>', HostDetailAPI.as_view()),

    path('admin/meters', MeterAPI.as_view()),

    path('admin/registers', RegisterAPI.as_view()),

    path('admin/measurements', MeasurementAPI.as_view()),

    path('admin/users', UserAPI.as_view()),
    path('admin/users/<int:pk>', UserDetailAPI.as_view())
]